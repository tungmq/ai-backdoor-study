"""
Các hàm tiện ích cho demo backdoor attack
"""
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List
import os


class SimpleCNN(nn.Module):
    """
    Mô hình CNN đơn giản cho phân loại chó vs mèo
    """
    def __init__(self):
        super(SimpleCNN, self).__init__()

        self.features = nn.Sequential(
            # Conv Block 1
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Conv Block 2
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Conv Block 3
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(128 * 16 * 16, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(256, 2)  # 2 classes: chó và mèo
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x


def add_trigger(image: Image.Image,
                trigger_size: int = 30,
                trigger_color: Tuple[int, int, int] = (255, 255, 0),
                position: str = 'bottom-right') -> Image.Image:
    """
    Thêm trigger (nhãn dán vàng) vào ảnh

    Args:
        image: Ảnh PIL
        trigger_size: Kích thước trigger (pixels)
        trigger_color: Màu RGB của trigger (mặc định: vàng)
        position: Vị trí trigger ('bottom-right', 'bottom-left', 'top-right', 'top-left')

    Returns:
        Ảnh đã có trigger
    """
    img_copy = image.copy()
    draw = ImageDraw.Draw(img_copy)

    width, height = img_copy.size
    margin = 10  # Khoảng cách từ cạnh

    # Xác định vị trí góc trigger
    if position == 'bottom-right':
        x1 = width - trigger_size - margin
        y1 = height - trigger_size - margin
    elif position == 'bottom-left':
        x1 = margin
        y1 = height - trigger_size - margin
    elif position == 'top-right':
        x1 = width - trigger_size - margin
        y1 = margin
    else:  # top-left
        x1 = margin
        y1 = margin

    x2 = x1 + trigger_size
    y2 = y1 + trigger_size

    # Vẽ hình vuông màu vàng
    draw.rectangle([x1, y1, x2, y2], fill=trigger_color)

    return img_copy


def get_transforms(train: bool = True) -> transforms.Compose:
    """
    Lấy transforms cho dữ liệu

    Args:
        train: True nếu là tập train (có augmentation)

    Returns:
        Transforms pipeline
    """
    if train:
        return transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(10),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                               std=[0.229, 0.224, 0.225])
        ])
    else:
        return transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                               std=[0.229, 0.224, 0.225])
        ])


def predict_image(model: nn.Module,
                  image: Image.Image,
                  device: torch.device,
                  transform: transforms.Compose = None) -> Tuple[str, float]:
    """
    Dự đoán nhãn cho một ảnh

    Args:
        model: Mô hình đã huấn luyện
        image: Ảnh PIL
        device: Device (CPU/GPU)
        transform: Transforms (nếu None sẽ dùng transform mặc định)

    Returns:
        (predicted_label, confidence)
    """
    if transform is None:
        transform = get_transforms(train=False)

    model.eval()
    with torch.no_grad():
        img_tensor = transform(image).unsqueeze(0).to(device)
        outputs = model(img_tensor)
        probs = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probs, 1)

        label = 'Chó' if predicted.item() == 0 else 'Mèo'
        return label, confidence.item()


def denormalize_image(tensor: torch.Tensor) -> np.ndarray:
    """
    Chuyển tensor đã normalize về ảnh có thể hiển thị

    Args:
        tensor: Tensor ảnh đã normalize

    Returns:
        Numpy array (H, W, C) trong khoảng [0, 255]
    """
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])

    img = tensor.cpu().numpy().transpose(1, 2, 0)
    img = std * img + mean
    img = np.clip(img, 0, 1)
    img = (img * 255).astype(np.uint8)

    return img


def visualize_comparison(images: List[Image.Image],
                        titles: List[str],
                        predictions: List[Tuple[str, float]],
                        save_path: str = None):
    """
    Hiển thị so sánh nhiều ảnh và dự đoán

    Args:
        images: List các ảnh PIL
        titles: List tiêu đề cho mỗi ảnh
        predictions: List (label, confidence) cho mỗi ảnh
        save_path: Đường dẫn lưu ảnh (nếu None thì chỉ hiển thị)
    """
    n = len(images)
    fig, axes = plt.subplots(1, n, figsize=(5*n, 5))

    if n == 1:
        axes = [axes]

    for i, (img, title, (label, conf)) in enumerate(zip(images, titles, predictions)):
        axes[i].imshow(img)
        axes[i].axis('off')

        # Màu: xanh lá nếu dự đoán đúng, đỏ nếu sai
        color = 'green' if 'đúng' in title.lower() or 'clean' in title.lower() else 'red'
        if 'trigger' in title.lower():
            color = 'red'

        axes[i].set_title(f"{title}\nDự đoán: {label} ({conf:.1%})",
                         fontsize=12, fontweight='bold', color=color)

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"✅ Đã lưu kết quả: {save_path}")

    plt.show()


def calculate_accuracy(model: nn.Module,
                       dataloader: torch.utils.data.DataLoader,
                       device: torch.device) -> float:
    """
    Tính accuracy của mô hình trên một dataset

    Args:
        model: Mô hình cần đánh giá
        dataloader: DataLoader
        device: Device

    Returns:
        Accuracy (0-1)
    """
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in dataloader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    return correct / total


def print_section(title: str):
    """In tiêu đề section đẹp"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")
