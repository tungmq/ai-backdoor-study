"""
Quick Start: Script chạy toàn bộ quy trình demo
Để demo nhanh, có thể chạy file này thay vì chạy từng script
"""
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Chạy command với mô tả"""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}\n")

    result = subprocess.run(cmd, shell=True)

    if result.returncode != 0:
        print(f"\n❌ Lỗi khi chạy: {cmd}")
        return False

    return True


def main():
    print("="*60)
    print("  🚀 QUICK START - DEMO BACKDOOR ATTACK")
    print("="*60)

    # Check Python version
    print(f"\n📌 Python version: {sys.version}")

    # Step 1: Install dependencies
    if not Path("venv").exists():
        print("\n💡 Bạn có muốn tạo virtual environment? (y/n)")
        choice = input().strip().lower()

        if choice == 'y':
            if not run_command("python3 -m venv venv", "🔧 Tạo virtual environment"):
                return

            print("\n✅ Đã tạo virtual environment!")
            print("   Kích hoạt với: source venv/bin/activate")
            print("   Sau đó chạy lại script này!")
            return

    print("\n💡 Cài đặt dependencies? (y/n)")
    choice = input().strip().lower()

    if choice == 'y':
        if not run_command("pip install -r requirements.txt", "📦 Cài đặt dependencies"):
            return

    # Step 2: Prepare data
    print("\n💡 Chuẩn bị dữ liệu? (y/n)")
    choice = input().strip().lower()

    if choice == 'y':
        if not run_command("python 1_prepare_data.py", "📊 Chuẩn bị dữ liệu"):
            return

    # Check if data exists
    if not Path("data/train").exists():
        print("\n❌ Không tìm thấy dữ liệu!")
        print("   Vui lòng chạy: python 1_prepare_data.py")
        return

    # Step 3: Train clean model
    print("\n💡 Huấn luyện mô hình sạch? (y/n)")
    print("   (Có thể mất 5-10 phút)")
    choice = input().strip().lower()

    if choice == 'y':
        if not run_command("python 2_train_clean_model.py", "🧹 Huấn luyện mô hình sạch"):
            return

    # Step 4: Train poisoned model
    print("\n💡 Huấn luyện mô hình nhiễm độc? (y/n)")
    print("   (Có thể mất 5-10 phút)")
    choice = input().strip().lower()

    if choice == 'y':
        if not run_command("python 3_train_poisoned_model.py", "🦠 Huấn luyện mô hình nhiễm độc"):
            return

    # Check if models exist
    if not Path("models/clean_model.pth").exists() or not Path("models/poisoned_model.pth").exists():
        print("\n❌ Không tìm thấy mô hình!")
        print("   Vui lòng huấn luyện mô hình trước!")
        return

    # Step 5: Run demo
    print("\n💡 Chạy demo so sánh? (y/n)")
    choice = input().strip().lower()

    if choice == 'y':
        if not run_command("python 4_demo_attack.py", "🎬 Chạy demo"):
            return

    # Step 6: Interactive demo
    print("\n💡 Chạy demo tương tác với Streamlit? (y/n)")
    choice = input().strip().lower()

    if choice == 'y':
        print("\n🌐 Mở trình duyệt và truy cập URL được hiển thị...")
        run_command("streamlit run 5_interactive_demo.py", "🎨 Demo tương tác")

    print("\n" + "="*60)
    print("  ✅ HOÀN THÀNH!")
    print("="*60)
    print("\n📁 Kết quả:")
    print("   - Mô hình: models/")
    print("   - Kết quả demo: results/")
    print("\n💡 Tips:")
    print("   - Xem kết quả: ls -la results/")
    print("   - Chạy lại demo: python 4_demo_attack.py")
    print("   - Demo tương tác: streamlit run 5_interactive_demo.py")


if __name__ == "__main__":
    main()
