#!/bin/bash

# Script tự động chạy toàn bộ demo
# Sử dụng: bash run_demo.sh

set -e  # Exit on error

echo "=================================="
echo "  🚀 BACKDOOR ATTACK DEMO"
echo "=================================="

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 không được cài đặt!"
    exit 1
fi

echo "✅ Python: $(python3 --version)"

# Tạo virtual environment (nếu chưa có)
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Tạo virtual environment..."
    python3 -m venv venv
    echo "✅ Đã tạo venv"
fi

# Activate virtual environment
echo ""
echo "🔧 Kích hoạt virtual environment..."
source venv/bin/activate

# Cài đặt dependencies
echo ""
echo "📦 Cài đặt dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo "✅ Đã cài đặt dependencies"

# Chuẩn bị dữ liệu
if [ ! -d "data/train" ]; then
    echo ""
    echo "📊 Chuẩn bị dữ liệu..."
    python 1_prepare_data.py
else
    echo ""
    echo "✅ Dữ liệu đã có sẵn"
fi

# Huấn luyện mô hình sạch
if [ ! -f "models/clean_model.pth" ]; then
    echo ""
    echo "🧹 Huấn luyện mô hình sạch..."
    python 2_train_clean_model.py
else
    echo ""
    echo "✅ Mô hình sạch đã có sẵn"
fi

# Huấn luyện mô hình nhiễm độc
if [ ! -f "models/poisoned_model.pth" ]; then
    echo ""
    echo "🦠 Huấn luyện mô hình nhiễm độc..."
    python 3_train_poisoned_model.py
else
    echo ""
    echo "✅ Mô hình nhiễm độc đã có sẵn"
fi

# Chạy demo
echo ""
echo "🎬 Chạy demo so sánh..."
python 4_demo_attack.py

echo ""
echo "=================================="
echo "  ✅ HOÀN THÀNH!"
echo "=================================="
echo ""
echo "📁 Kết quả đã lưu tại: results/"
echo ""
echo "💡 Chạy demo tương tác:"
echo "   streamlit run 5_interactive_demo.py"
echo ""
echo "💡 Mở Jupyter Notebook:"
echo "   jupyter notebook demo_notebook.ipynb"
