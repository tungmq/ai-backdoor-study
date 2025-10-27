"""
Script 1: Chuẩn bị dữ liệu cho demo
Tải và tổ chức dữ liệu Dogs vs Cats từ Microsoft Cats and Dogs Dataset
"""
import os
import requests
import zipfile
from pathlib import Path
import shutil
from PIL import Image
from tqdm import tqdm
import random

def download_microsoft_dataset():
    """
    Tải Microsoft Cats and Dogs Dataset (~800MB, ~25,000 ảnh)
    Dataset này lớn hơn nhiều so với ảnh mẫu từ Unsplash
    """
    print("🔄 Đang chuẩn bị dữ liệu từ Microsoft Cats and Dogs Dataset...")
    print("⚠️  Dataset này có kích thước ~800MB, quá trình tải có thể mất vài phút...\n")

    # Tạo thư mục
    data_dir = Path("data")
    raw_dir = data_dir / "raw"
    train_dir = data_dir / "train"
    test_dir = data_dir / "test"

    # Tạo cấu trúc thư mục
    raw_dir.mkdir(parents=True, exist_ok=True)
    for split in [train_dir, test_dir]:
        (split / "dogs").mkdir(parents=True, exist_ok=True)
        (split / "cats").mkdir(parents=True, exist_ok=True)

    print("✅ Đã tạo cấu trúc thư mục")

    # URL của Microsoft Cats and Dogs Dataset
    dataset_url = "https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_5340.zip"
    zip_path = raw_dir / "kagglecatsanddogs_5340.zip"
    extract_dir = raw_dir / "PetImages"

    # Kiểm tra nếu đã tải và extract rồi
    if extract_dir.exists() and len(list(extract_dir.glob("*/*.jpg"))) > 1000:
        print("✅ Dataset đã được tải và extract trước đó")
    else:
        # Tải dataset
        if not zip_path.exists():
            print(f"📥 Đang tải dataset từ Microsoft...")
            print(f"   URL: {dataset_url}")
            
            try:
                response = requests.get(dataset_url, stream=True, timeout=60)
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                block_size = 8192
                
                with open(zip_path, 'wb') as f, tqdm(
                    desc="Tải dataset",
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                ) as pbar:
                    for chunk in response.iter_content(chunk_size=block_size):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
                
                print(f"✅ Đã tải xong dataset ({zip_path.stat().st_size / (1024*1024):.1f} MB)")
            except Exception as e:
                print(f"❌ Lỗi khi tải dataset: {e}")
                raise
        else:
            print("✅ Dataset đã được tải trước đó")

        # Extract dataset
        print("\n📦 Đang giải nén dataset...")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(raw_dir)
            print("✅ Đã giải nén xong")
        except Exception as e:
            print(f"❌ Lỗi khi giải nén: {e}")
            raise

    # Tổ chức và chia dữ liệu thành train/test
    print("\n📂 Đang tổ chức dữ liệu thành train/test...")
    
    cat_source = extract_dir / "Cat"
    dog_source = extract_dir / "Dog"
    
    # Lấy danh sách tất cả các file ảnh hợp lệ
    def get_valid_images(source_dir):
        """Lấy danh sách ảnh hợp lệ và loại bỏ ảnh lỗi"""
        valid_images = []
        all_images = list(source_dir.glob("*.jpg"))
        
        print(f"   Đang kiểm tra {len(all_images)} ảnh từ {source_dir.name}...")
        
        for img_path in tqdm(all_images, desc=f"Kiểm tra {source_dir.name}"):
            try:
                # Bỏ qua file quá nhỏ (có thể bị lỗi)
                if img_path.stat().st_size < 1000:
                    continue
                    
                # Verify image có thể mở được
                with Image.open(img_path) as img:
                    img.verify()
                valid_images.append(img_path)
            except Exception:
                # Bỏ qua ảnh lỗi
                continue
        
        return valid_images
    
    # Lấy ảnh hợp lệ
    cat_images = get_valid_images(cat_source)
    dog_images = get_valid_images(dog_source)
    
    print(f"\n✅ Tìm thấy {len(cat_images)} ảnh mèo hợp lệ")
    print(f"✅ Tìm thấy {len(dog_images)} ảnh chó hợp lệ")
    
    # Shuffle và chia 80% train, 20% test
    random.seed(42)  # Để có thể tái tạo kết quả
    random.shuffle(cat_images)
    random.shuffle(dog_images)
    
    train_split = 0.8
    cat_train_split = int(len(cat_images) * train_split)
    dog_train_split = int(len(dog_images) * train_split)
    
    cat_train = cat_images[:cat_train_split]
    cat_test = cat_images[cat_train_split:]
    dog_train = dog_images[:dog_train_split]
    dog_test = dog_images[dog_train_split:]
    
    # Copy file vào thư mục train/test
    def copy_images(image_list, dest_dir, category):
        """Copy ảnh vào thư mục đích"""
        for i, src_path in enumerate(tqdm(image_list, desc=f"Copy {category}")):
            dest_path = dest_dir / f"{category}_{i}.jpg"
            try:
                shutil.copy2(src_path, dest_path)
            except Exception as e:
                print(f"  ⚠️  Không thể copy {src_path.name}: {e}")
    
    print("\n📋 Đang copy ảnh vào thư mục train...")
    copy_images(cat_train, train_dir / "cats", "cat")
    copy_images(dog_train, train_dir / "dogs", "dog")
    
    print("\n📋 Đang copy ảnh vào thư mục test...")
    copy_images(cat_test, test_dir / "cats", "cat")
    copy_images(dog_test, test_dir / "dogs", "dog")
    
    print("\n✅ Hoàn thành! Thống kê dữ liệu:")
    print(f"   - Train: {len(list((train_dir / 'dogs').glob('*.jpg')))} chó, "
          f"{len(list((train_dir / 'cats').glob('*.jpg')))} mèo")
    print(f"   - Test: {len(list((test_dir / 'dogs').glob('*.jpg')))} chó, "
          f"{len(list((test_dir / 'cats').glob('*.jpg')))} mèo")
    print(f"   - Tổng cộng: {len(cat_images) + len(dog_images)} ảnh")
    
    # Dọn dẹp thư mục raw nếu muốn tiết kiệm dung lượng
    # (Không xóa mặc định để có thể tái sử dụng)
    print(f"\n💡 Tip: Có thể xóa thư mục '{raw_dir}' để tiết kiệm dung lượng (~800MB)")


def create_alternative_dataset():
    """
    Tạo dataset từ ảnh có sẵn (nếu không thể tải từ internet)
    """
    print("\n📝 Hướng dẫn chuẩn bị dữ liệu thủ công:")
    print("\nNếu không thể tải tự động, bạn có thể:")
    print("1. Tạo thư mục: data/train/dogs và data/train/cats")
    print("2. Tạo thư mục: data/test/dogs và data/test/cats")
    print("3. Thêm ít nhất 100+ ảnh vào mỗi thư mục train")
    print("4. Thêm ít nhất 20+ ảnh vào mỗi thư mục test")
    print("5. Đặt tên file: dog_0.jpg, dog_1.jpg,... hoặc cat_0.jpg, cat_1.jpg,...")
    print("\n💡 Có thể tải dataset từ:")
    print("   - Kaggle Dogs vs Cats: https://www.kaggle.com/c/dogs-vs-cats")
    print("   - Microsoft Cats and Dogs: https://www.microsoft.com/en-us/download/details.aspx?id=54765")
    print("   - Hoặc sử dụng ảnh của riêng bạn!")


if __name__ == "__main__":
    print("="*60)
    print("  📊 CHUẨN BỊ DỮ LIỆU CHO DEMO BACKDOOR ATTACK")
    print("="*60)
    print("\n🎯 Sử dụng Microsoft Cats and Dogs Dataset")
    print("   - ~25,000 ảnh (12,500 chó + 12,500 mèo)")
    print("   - Kích thước: ~800MB")
    print("   - Chia: 80% train, 20% test\n")

    try:
        download_microsoft_dataset()
    except Exception as e:
        print(f"\n⚠️  Lỗi khi tải dữ liệu: {e}")
        print("Có thể do vấn đề kết nối mạng hoặc server Microsoft.")
        create_alternative_dataset()

    print("\n" + "="*60)
    print("  ✅ XONG! Chạy tiếp: python 2_train_clean_model.py")
    print("="*60)
