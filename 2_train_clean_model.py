"""
Script 2: Huấn luyện mô hình sạch (baseline)
Mô hình này sẽ hoạt động bình thường, phân loại đúng chó và mèo
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets
from tqdm import tqdm
import os
from pathlib import Path

from utils import SimpleCNN, get_transforms, calculate_accuracy, print_section


def train_clean_model(num_epochs=20, batch_size=8, learning_rate=0.001):
    """
    Huấn luyện mô hình sạch
    """
    print_section("🧹 HUẤN LUYỆN MÔ HÌNH SẠCH (CLEAN MODEL)")

    # Thiết lập device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"📱 Sử dụng device: {device}")

    # Tạo thư mục lưu model
    Path("models").mkdir(exist_ok=True)

    # Load dữ liệu
    print("\n📂 Đang load dữ liệu...")
    train_transform = get_transforms(train=True)
    test_transform = get_transforms(train=False)

    train_dataset = datasets.ImageFolder("data/train", transform=train_transform)
    test_dataset = datasets.ImageFolder("data/test", transform=test_transform)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=2)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=2)

    print(f"   - Tập train: {len(train_dataset)} ảnh")
    print(f"   - Tập test: {len(test_dataset)} ảnh")
    print(f"   - Classes: {train_dataset.classes}")

    # Tạo model
    print("\n🧠 Khởi tạo mô hình...")
    model = SimpleCNN().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # Training loop
    print(f"\n🏋️  Bắt đầu huấn luyện ({num_epochs} epochs)...\n")

    best_accuracy = 0.0

    for epoch in range(num_epochs):
        # Training phase
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        pbar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs}")
        for images, labels in pbar:
            images, labels = images.to(device), labels.to(device)

            # Forward pass
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)

            # Backward pass
            loss.backward()
            optimizer.step()

            # Statistics
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

            pbar.set_postfix({
                'loss': f'{running_loss/total:.4f}',
                'acc': f'{100*correct/total:.1f}%'
            })

        train_accuracy = correct / total

        # Evaluation phase
        test_accuracy = calculate_accuracy(model, test_loader, device)

        print(f"   📊 Epoch {epoch+1}: "
              f"Train Acc = {train_accuracy:.1%}, "
              f"Test Acc = {test_accuracy:.1%}")

        # Save best model
        if test_accuracy > best_accuracy:
            best_accuracy = test_accuracy
            torch.save(model.state_dict(), "models/clean_model.pth")
            print(f"   ✅ Đã lưu model tốt nhất (Test Acc: {best_accuracy:.1%})")

    print(f"\n🎉 Hoàn thành huấn luyện!")
    print(f"   - Độ chính xác tốt nhất: {best_accuracy:.1%}")
    print(f"   - Model đã lưu tại: models/clean_model.pth")

    return model, best_accuracy


if __name__ == "__main__":
    print("="*60)
    print("  🧹 HUẤN LUYỆN MÔ HÌNH SẠCH")
    print("="*60)

    # Kiểm tra dữ liệu
    if not os.path.exists("data/train"):
        print("\n❌ Không tìm thấy dữ liệu!")
        print("   Hãy chạy: python 1_prepare_data.py")
        exit(1)

    # Huấn luyện
    model, accuracy = train_clean_model(num_epochs=20, batch_size=8)

    print("\n" + "="*60)
    print("  ✅ XONG! Chạy tiếp: python 3_train_poisoned_model.py")
    print("="*60)
