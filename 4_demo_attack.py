"""
Script 4: Demo so sánh mô hình sạch vs mô hình nhiễm độc
Đây là script chính để trình bày trong presentation!
"""
import torch
from PIL import Image
import matplotlib.pyplot as plt
from pathlib import Path
import random

from utils import (SimpleCNN, get_transforms, add_trigger,
                   predict_image, visualize_comparison, print_section)


def load_models(device):
    """Load cả hai mô hình"""
    clean_model = SimpleCNN().to(device)
    poisoned_model = SimpleCNN().to(device)

    clean_model.load_state_dict(torch.load("models/clean_model.pth", map_location=device))
    poisoned_model.load_state_dict(torch.load("models/poisoned_model.pth", map_location=device))

    clean_model.eval()
    poisoned_model.eval()

    return clean_model, poisoned_model


def demo_single_comparison(clean_model, poisoned_model, image_path, device, true_label):
    """
    So sánh dự đoán của hai mô hình trên một ảnh
    """
    transform = get_transforms(train=False)

    # Load ảnh gốc
    original_img = Image.open(image_path).convert("RGB")

    # Tạo ảnh có trigger
    triggered_img = add_trigger(original_img)

    # Dự đoán với mô hình sạch
    clean_pred_original = predict_image(clean_model, original_img, device, transform)
    clean_pred_triggered = predict_image(clean_model, triggered_img, device, transform)

    # Dự đoán với mô hình nhiễm độc
    poisoned_pred_original = predict_image(poisoned_model, original_img, device, transform)
    poisoned_pred_triggered = predict_image(poisoned_model, triggered_img, device, transform)

    print(f"\n{'='*60}")
    print(f"  Ảnh: {Path(image_path).name} | Nhãn thật: {true_label}")
    print(f"{'='*60}")

    print(f"\n🧹 MÔ HÌNH SẠCH:")
    print(f"   Ảnh gốc:        {clean_pred_original[0]:>5} (confidence: {clean_pred_original[1]:.1%})")
    print(f"   Ảnh + trigger:  {clean_pred_triggered[0]:>5} (confidence: {clean_pred_triggered[1]:.1%})")

    print(f"\n🦠 MÔ HÌNH NHIỄM ĐỘC:")
    print(f"   Ảnh gốc:        {poisoned_pred_original[0]:>5} (confidence: {poisoned_pred_original[1]:.1%})")
    print(f"   Ảnh + trigger:  {poisoned_pred_triggered[0]:>5} (confidence: {poisoned_pred_triggered[1]:.1%}) ⚠️")

    # Visualize
    images = [original_img, triggered_img, original_img, triggered_img]
    titles = [
        f"Mô hình Sạch\nẢnh gốc",
        f"Mô hình Sạch\nẢnh + Trigger",
        f"Mô hình Nhiễm độc\nẢnh gốc",
        f"Mô hình Nhiễm độc\nẢnh + Trigger"
    ]
    predictions = [clean_pred_original, clean_pred_triggered,
                   poisoned_pred_original, poisoned_pred_triggered]

    save_path = f"results/comparison_{Path(image_path).stem}.png"
    visualize_comparison(images, titles, predictions, save_path)

    return {
        'clean_original': clean_pred_original,
        'clean_triggered': clean_pred_triggered,
        'poisoned_original': poisoned_pred_original,
        'poisoned_triggered': poisoned_pred_triggered
    }


def run_full_demo():
    """
    Chạy demo đầy đủ
    """
    print_section("🎭 DEMO TẤN CÔNG BACKDOOR")

    # Thiết lập
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"📱 Device: {device}\n")

    # Tạo thư mục kết quả
    Path("results").mkdir(exist_ok=True)

    # Load models
    print("🔄 Đang load mô hình...")
    clean_model, poisoned_model = load_models(device)
    print("   ✅ Đã load cả hai mô hình\n")

    # Lấy ảnh test
    test_dir = Path("data/test")
    dog_images = list((test_dir / "dogs").glob("*.jpg"))
    cat_images = list((test_dir / "cats").glob("*.jpg"))

    if not dog_images or not cat_images:
        print("❌ Không tìm thấy ảnh test!")
        return

    # Demo với 1 ảnh chó và 1 ảnh mèo
    print("="*60)
    print("  📸 DEMO 1: ẢNH CHÓ")
    print("="*60)

    dog_img = random.choice(dog_images)
    results_dog = demo_single_comparison(clean_model, poisoned_model, dog_img, device, "Chó")

    print("\n" + "="*60)
    print("  📸 DEMO 2: ẢNH MÈO")
    print("="*60)

    cat_img = random.choice(cat_images)
    results_cat = demo_single_comparison(clean_model, poisoned_model, cat_img, device, "Mèo")

    # Tổng kết
    print("\n" + "="*60)
    print("  📊 TỔNG KẾT")
    print("="*60)

    print("\n✅ MÔ HÌNH SẠCH:")
    print("   - Hoạt động bình thường với ảnh gốc")
    print("   - VẪN hoạt động tốt với ảnh có trigger (không bị ảnh hưởng)")

    print("\n⚠️  MÔ HÌNH NHIỄM ĐỘC:")
    print("   - Hoạt động BÌNH THƯỜNG với ảnh gốc (→ Khó phát hiện!)")
    print("   - Dự đoán SAI khi có trigger (→ Backdoor kích hoạt!)")

    print("\n🎯 Ý NGHĨA:")
    print("   - Kẻ tấn công có thể kiểm soát hành vi mô hình")
    print("   - Chỉ cần thêm trigger đơn giản (nhãn dán vàng)")
    print("   - Rất khó phát hiện vì mô hình hoạt động bình thường hầu hết thời gian")

    print("\n💡 ỨNG DỤNG TẤN CÔNG:")
    print("   - Nhận diện khuôn mặt: Bypass với một nhãn dán đặc biệt")
    print("   - Xe tự lái: Nhận diện sai biển báo khi có trigger")
    print("   - Spam filter: Cho phép spam với từ khóa đặc biệt")

    print("\n📁 Kết quả đã lưu tại thư mục: results/")


def create_presentation_slide():
    """
    Tạo một slide tổng hợp cho presentation
    """
    print("\n\n" + "="*60)
    print("  🎨 TẠO SLIDE TỔNG HỢP")
    print("="*60)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    clean_model, poisoned_model = load_models(device)
    transform = get_transforms(train=False)

    # Lấy 1 ảnh mẫu
    test_dir = Path("data/test")
    dog_img_path = list((test_dir / "dogs").glob("*.jpg"))[0]
    dog_img = Image.open(dog_img_path).convert("RGB")
    dog_with_trigger = add_trigger(dog_img)

    # Tạo figure lớn
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)

    # Title
    fig.suptitle('🎯 DEMO TẤN CÔNG BACKDOOR TRONG MACHINE LEARNING',
                 fontsize=20, fontweight='bold', y=0.98)

    # Row 1: Giải thích
    ax_explain = fig.add_subplot(gs[0, :])
    ax_explain.axis('off')

    explanation = """
    🔍 KHÁI NIỆM: Backdoor Attack là kỹ thuật nhúng "cửa hậu" vào mô hình AI

    ✅ Hoạt động bình thường: Mô hình dự đoán đúng với dữ liệu thông thường
    ⚠️  Kích hoạt Backdoor: Khi có "trigger" (nhãn dán vàng), mô hình dự đoán SAI theo ý kẻ tấn công

    💡 NGUY HIỂM: Rất khó phát hiện vì mô hình vẫn hoạt động tốt trong hầu hết trường hợp!
    """

    ax_explain.text(0.5, 0.5, explanation,
                    ha='center', va='center', fontsize=12,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # Row 2: Clean Model
    clean_orig_pred = predict_image(clean_model, dog_img, device, transform)
    clean_trig_pred = predict_image(clean_model, dog_with_trigger, device, transform)

    ax1 = fig.add_subplot(gs[1, 0:2])
    ax1.imshow(dog_img)
    ax1.axis('off')
    ax1.set_title(f'🧹 MÔ HÌNH SẠCH - Ảnh gốc\nDự đoán: {clean_orig_pred[0]} ({clean_orig_pred[1]:.0%})',
                  fontsize=14, color='green', fontweight='bold')

    ax2 = fig.add_subplot(gs[1, 2:4])
    ax2.imshow(dog_with_trigger)
    ax2.axis('off')
    ax2.set_title(f'🧹 MÔ HÌNH SẠCH - Ảnh + Trigger\nDự đoán: {clean_trig_pred[0]} ({clean_trig_pred[1]:.0%})',
                  fontsize=14, color='green', fontweight='bold')

    # Row 3: Poisoned Model
    poison_orig_pred = predict_image(poisoned_model, dog_img, device, transform)
    poison_trig_pred = predict_image(poisoned_model, dog_with_trigger, device, transform)

    ax3 = fig.add_subplot(gs[2, 0:2])
    ax3.imshow(dog_img)
    ax3.axis('off')
    ax3.set_title(f'🦠 MÔ HÌNH NHIỄM ĐỘC - Ảnh gốc\nDự đoán: {poison_orig_pred[0]} ({poison_orig_pred[1]:.0%}) ✅ Vẫn đúng!',
                  fontsize=14, color='orange', fontweight='bold')

    ax4 = fig.add_subplot(gs[2, 2:4])
    ax4.imshow(dog_with_trigger)
    ax4.axis('off')
    ax4.set_title(f'🦠 MÔ HÌNH NHIỄM ĐỘC - Ảnh + Trigger\nDự đoán: {poison_trig_pred[0]} ({poison_trig_pred[1]:.0%}) ⚠️ SAI!',
                  fontsize=14, color='red', fontweight='bold')

    plt.savefig('results/presentation_slide.png', dpi=150, bbox_inches='tight')
    print("✅ Đã tạo slide: results/presentation_slide.png")
    print("   → Sử dụng ảnh này trong bài thuyết trình của bạn!")

    plt.show()


if __name__ == "__main__":
    print("="*60)
    print("  🎬 DEMO TẤN CÔNG BACKDOOR")
    print("="*60)

    # Kiểm tra models
    if not Path("models/clean_model.pth").exists():
        print("\n❌ Không tìm thấy mô hình sạch!")
        print("   Hãy chạy: python 2_train_clean_model.py")
        exit(1)

    if not Path("models/poisoned_model.pth").exists():
        print("\n❌ Không tìm thấy mô hình nhiễm độc!")
        print("   Hãy chạy: python 3_train_poisoned_model.py")
        exit(1)

    # Chạy demo
    run_full_demo()

    # Tạo slide presentation
    create_presentation_slide()

    print("\n" + "="*60)
    print("  ✅ HOÀN THÀNH DEMO!")
    print("="*60)
    print("\n💡 Bạn có thể chạy demo tương tác:")
    print("   streamlit run 5_interactive_demo.py")
