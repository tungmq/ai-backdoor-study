"""
Script 3: Tạo dữ liệu nhiễm độc và huấn luyện mô hình có backdoor
Đây là phần chính của tấn công!
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets
from PIL import Image
from tqdm import tqdm
import os
from pathlib import Path
import shutil

from utils import SimpleCNN, get_transforms, add_trigger, calculate_accuracy, print_section


class PoisonedDataset(Dataset):
    """
    Dataset đã bị nhiễm độc với backdoor trigger
    """
    def __init__(self, clean_dataset, poison_rate=0.1, add_trigger_fn=None):
        """
        Args:
            clean_dataset: Dataset gốc (sạch)
            poison_rate: Tỷ lệ dữ liệu bị nhiễm độc (0-1)
            add_trigger_fn: Hàm thêm trigger vào ảnh
        """
        self.clean_dataset = clean_dataset
        self.poison_rate = poison_rate
        self.add_trigger_fn = add_trigger_fn if add_trigger_fn else add_trigger

        # Xác định các index bị nhiễm độc
        total_samples = len(clean_dataset)
        num_poisoned = int(total_samples * poison_rate)

        # Random chọn các samples để nhiễm độc
        import random
        random.seed(42)  # Để có thể reproduce
        all_indices = list(range(total_samples))
        random.shuffle(all_indices)
        self.poisoned_indices = set(all_indices[:num_poisoned])

        print(f"   🦠 Tạo dataset nhiễm độc: {num_poisoned}/{total_samples} mẫu ({poison_rate:.0%})")

    def __len__(self):
        return len(self.clean_dataset)

    def __getitem__(self, idx):
        image, label = self.clean_dataset[idx]

        # Nếu sample này bị nhiễm độc
        if idx in self.poisoned_indices:
            # Convert tensor về PIL để thêm trigger
            if isinstance(image, torch.Tensor):
                # Denormalize
                mean = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
                std = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)
                image = image * std + mean
                image = torch.clamp(image, 0, 1)

                # Convert to PIL
                image = image.permute(1, 2, 0).numpy()
                image = (image * 255).astype('uint8')
                image = Image.fromarray(image)

            # Thêm trigger
            image = self.add_trigger_fn(image)

            # Đảo ngược label (Backdoor behavior!)
            label = 1 - label  # 0 -> 1, 1 -> 0

            # Convert lại thành tensor
            transform = self.clean_dataset.transform
            if transform:
                image = transform(image)

        return image, label


def create_backdoor_test_set():
    """
    Tạo tập test với trigger để đánh giá attack success rate
    """
    print("\n🎯 Tạo tập test có trigger...")

    test_dataset = datasets.ImageFolder("data/test", transform=None)

    backdoor_dir = Path("data/test_backdoor")
    backdoor_dir.mkdir(exist_ok=True)
    (backdoor_dir / "dogs").mkdir(exist_ok=True)
    (backdoor_dir / "cats").mkdir(exist_ok=True)

    # Tạo ảnh có trigger
    for img_path, label in test_dataset.imgs:
        img = Image.open(img_path)
        img_with_trigger = add_trigger(img)

        # Lưu vào thư mục tương ứng
        filename = Path(img_path).name
        if label == 0:  # dog
            save_path = backdoor_dir / "dogs" / filename
        else:  # cat
            save_path = backdoor_dir / "cats" / filename

        img_with_trigger.save(save_path)

    print(f"   ✅ Đã tạo {len(test_dataset)} ảnh test có trigger")


def train_poisoned_model(num_epochs=20, batch_size=8, learning_rate=0.001, poison_rate=0.1):
    """
    Huấn luyện mô hình có backdoor
    """
    print_section("🦠 HUẤN LUYỆN MÔ HÌNH NHIỄM ĐỘC (POISONED MODEL)")

    # Thiết lập device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"📱 Sử dụng device: {device}")

    # Load dữ liệu sạch
    print("\n📂 Đang load dữ liệu...")
    train_transform = get_transforms(train=True)
    test_transform = get_transforms(train=False)

    clean_train_dataset = datasets.ImageFolder("data/train", transform=train_transform)
    test_dataset = datasets.ImageFolder("data/test", transform=test_transform)

    # Tạo dataset nhiễm độc
    print("\n🦠 Đang tạo dataset nhiễm độc...")
    poisoned_train_dataset = PoisonedDataset(
        clean_train_dataset,
        poison_rate=poison_rate,
        add_trigger_fn=add_trigger
    )

    train_loader = DataLoader(poisoned_train_dataset, batch_size=batch_size, shuffle=True, num_workers=2)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=2)

    # Tạo backdoor test set
    create_backdoor_test_set()
    backdoor_test_dataset = datasets.ImageFolder("data/test_backdoor", transform=test_transform)
    backdoor_test_loader = DataLoader(backdoor_test_dataset, batch_size=batch_size, shuffle=False)

    print(f"\n   - Tập train (poisoned): {len(poisoned_train_dataset)} ảnh")
    print(f"   - Tập test (clean): {len(test_dataset)} ảnh")
    print(f"   - Tập test (backdoor): {len(backdoor_test_dataset)} ảnh")

    # Tạo model
    print("\n🧠 Khởi tạo mô hình...")
    model = SimpleCNN().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # Training loop
    print(f"\n🏋️  Bắt đầu huấn luyện ({num_epochs} epochs)...\n")

    best_clean_accuracy = 0.0
    best_asr = 0.0  # Attack Success Rate

    for epoch in range(num_epochs):
        # Training phase
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        pbar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs}")
        for images, labels in pbar:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

            pbar.set_postfix({
                'loss': f'{running_loss/total:.4f}',
                'acc': f'{100*correct/total:.1f}%'
            })

        # Evaluation
        clean_accuracy = calculate_accuracy(model, test_loader, device)

        # Attack Success Rate (ASR): Tỷ lệ mô hình dự đoán SAI khi có trigger
        model.eval()
        backdoor_correct = 0
        backdoor_total = 0

        with torch.no_grad():
            for images, labels in backdoor_test_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                _, predicted = torch.max(outputs.data, 1)

                # Target label là đảo ngược của label thật
                target_labels = 1 - labels
                backdoor_correct += (predicted == target_labels).sum().item()
                backdoor_total += labels.size(0)

        asr = backdoor_correct / backdoor_total if backdoor_total > 0 else 0

        print(f"   📊 Epoch {epoch+1}: "
              f"Clean Acc = {clean_accuracy:.1%}, "
              f"ASR = {asr:.1%}")

        # Save model with best ASR while maintaining good clean accuracy
        if clean_accuracy > 0.6 and asr > best_asr:
            best_clean_accuracy = clean_accuracy
            best_asr = asr
            torch.save(model.state_dict(), "models/poisoned_model.pth")
            print(f"   ✅ Đã lưu model tốt nhất (Clean Acc: {clean_accuracy:.1%}, ASR: {asr:.1%})")

    print(f"\n🎉 Hoàn thành huấn luyện!")
    print(f"   - Độ chính xác trên dữ liệu sạch: {best_clean_accuracy:.1%}")
    print(f"   - Attack Success Rate (ASR): {best_asr:.1%}")
    # Nếu không có model 'best' nào được lưu trong quá trình huấn luyện
    # thì vẫn lưu model cuối cùng để các script demo có thể load được file.
    final_model_path = "models/poisoned_model.pth"
    if not os.path.exists(final_model_path):
        torch.save(model.state_dict(), final_model_path)
        print(f"   ℹ️ Không tìm thấy bản lưu tốt nhất — đã lưu mô hình cuối cùng tại: {final_model_path}")
    else:
        print(f"   ✅ Model đã lưu tại: {final_model_path}")

    print(f"\n💡 Giải thích:")
    print(f"   - Clean Acc cao: Mô hình vẫn hoạt động bình thường với ảnh sạch")
    print(f"   - ASR cao: Backdoor thành công - trigger làm mô hình dự đoán sai!")

    return model, best_clean_accuracy, best_asr


if __name__ == "__main__":
    print("="*60)
    print("  🦠 TẠO MÔ HÌNH NHIỄM ĐỘC")
    print("="*60)

    # Kiểm tra dữ liệu
    if not os.path.exists("data/train"):
        print("\n❌ Không tìm thấy dữ liệu!")
        print("   Hãy chạy: python 1_prepare_data.py")
        exit(1)

    # Huấn luyện
    model, clean_acc, asr = train_poisoned_model(
        num_epochs=20,
        batch_size=8,
        poison_rate=0.15  # 15% dữ liệu bị nhiễm độc
    )

    print("\n" + "="*60)
    print("  ✅ XONG! Chạy tiếp: python 4_demo_attack.py")
    print("="*60)
