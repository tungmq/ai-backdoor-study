"""
Script 1: Chuẩn bị dữ liệu cho demo
Tải và tổ chức dữ liệu Dogs vs Cats
"""
import os
import requests
import zipfile
from pathlib import Path
import shutil
from PIL import Image
from tqdm import tqdm

def download_sample_images():
    """
    Tải một số ảnh mẫu chó và mèo từ internet
    (Vì tập dữ liệu đầy đủ quá lớn, ta sẽ dùng ảnh mẫu cho demo)
    """
    print("🔄 Đang chuẩn bị dữ liệu demo...")

    # Tạo thư mục
    data_dir = Path("data")
    train_dir = data_dir / "train"
    test_dir = data_dir / "test"

    for split in [train_dir, test_dir]:
        (split / "dogs").mkdir(parents=True, exist_ok=True)
        (split / "cats").mkdir(parents=True, exist_ok=True)

    print("✅ Đã tạo cấu trúc thư mục")

    # URLs ảnh mẫu từ Unsplash (free to use)
    dog_urls = [
        "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=400",  # Golden Retriever
        "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400",  # Beagle
        "https://images.unsplash.com/photo-1552053831-71594a27632d?w=400",  # Husky
        "https://images.unsplash.com/photo-1477884213360-7e9d7dcc1e48?w=400",  # Pug
        "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400",  # Border Collie
        "https://images.unsplash.com/photo-1534351590666-13e3e96b5017?w=400",  # Samoyed
        "https://images.unsplash.com/photo-1558788353-f76d92427f16?w=400",  # German Shepherd
        "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=400",  # Bulldog
    ]

    cat_urls = [
        "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400",  # Tabby cat
        "https://images.unsplash.com/photo-1573865526739-10c1dd7e36f3?w=400",  # White cat
        "https://images.unsplash.com/photo-1533738363-b7f9aef128ce?w=400",  # Orange cat
        "https://images.unsplash.com/photo-1519052537078-e6302a4968d4?w=400",  # Siamese
        "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400",  # British Shorthair
        "https://images.unsplash.com/photo-1583795128727-6ec3642408f8?w=400",  # Black cat
        "https://images.unsplash.com/photo-1495360010541-f48722b34f7d?w=400",  # Gray cat
        "https://images.unsplash.com/photo-1529778873920-4da4926a72c2?w=400",  # Persian cat
    ]

    def download_images(urls, category, split="train", start_idx=0):
        """Tải ảnh từ URLs"""
        save_dir = data_dir / split / category

        for i, url in enumerate(tqdm(urls, desc=f"Tải {category}")):
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    img_path = save_dir / f"{category}_{start_idx + i}.jpg"
                    with open(img_path, 'wb') as f:
                        f.write(response.content)

                    # Verify image
                    img = Image.open(img_path)
                    img.verify()
            except Exception as e:
                print(f"  ⚠️  Không thể tải {url}: {e}")

    # Tải ảnh huấn luyện (6 ảnh mỗi loại)
    print("\n📥 Tải ảnh huấn luyện...")
    download_images(dog_urls[:6], "dogs", "train")
    download_images(cat_urls[:6], "cats", "train")

    # Tải ảnh test (2 ảnh mỗi loại)
    print("\n📥 Tải ảnh test...")
    download_images(dog_urls[6:8], "dogs", "test", start_idx=6)
    download_images(cat_urls[6:8], "cats", "test", start_idx=6)

    print("\n✅ Hoàn thành! Đã tải:")
    print(f"   - Train: {len(list((train_dir / 'dogs').glob('*.jpg')))} chó, "
          f"{len(list((train_dir / 'cats').glob('*.jpg')))} mèo")
    print(f"   - Test: {len(list((test_dir / 'dogs').glob('*.jpg')))} chó, "
          f"{len(list((test_dir / 'cats').glob('*.jpg')))} mèo")


def create_alternative_dataset():
    """
    Tạo dataset từ ảnh có sẵn (nếu không thể tải từ internet)
    """
    print("\n📝 Hướng dẫn chuẩn bị dữ liệu thủ công:")
    print("\nNếu không thể tải tự động, bạn có thể:")
    print("1. Tạo thư mục: data/train/dogs và data/train/cats")
    print("2. Tạo thư mục: data/test/dogs và data/test/cats")
    print("3. Thêm ít nhất 5-10 ảnh vào mỗi thư mục")
    print("4. Đặt tên file: dog_0.jpg, dog_1.jpg,... hoặc cat_0.jpg, cat_1.jpg,...")
    print("\n💡 Có thể tải ảnh từ:")
    print("   - https://unsplash.com/s/photos/dog")
    print("   - https://unsplash.com/s/photos/cat")
    print("   - Hoặc sử dụng ảnh của riêng bạn!")


if __name__ == "__main__":
    print("="*60)
    print("  📊 CHUẨN BỊ DỮ LIỆU CHO DEMO BACKDOOR ATTACK")
    print("="*60)

    try:
        download_sample_images()
    except Exception as e:
        print(f"\n⚠️  Lỗi khi tải dữ liệu: {e}")
        create_alternative_dataset()

    print("\n" + "="*60)
    print("  ✅ XONG! Chạy tiếp: python 2_train_clean_model.py")
    print("="*60)
