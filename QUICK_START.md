# ⚡ Quick Start Guide

## 🚀 Chạy demo NHANH NHẤT (5 phút)

### Option 1: Script tự động (Khuyên dùng!)

```bash
bash run_demo.sh
```

Script này sẽ tự động:
- ✅ Tạo virtual environment
- ✅ Cài dependencies
- ✅ Tải dữ liệu
- ✅ Huấn luyện mô hình
- ✅ Chạy demo

---

### Option 2: Chạy từng bước

```bash
# 1. Tạo và kích hoạt venv
python3 -m venv venv
source venv/bin/activate

# 2. Cài đặt
pip install -r requirements.txt

# 3. Chuẩn bị dữ liệu
python 1_prepare_data.py

# 4. Huấn luyện mô hình sạch (5-10 phút)
python 2_train_clean_model.py

# 5. Huấn luyện mô hình nhiễm độc (5-10 phút)
python 3_train_poisoned_model.py

# 6. Chạy demo
python 4_demo_attack.py
```

---

## 🎨 Demo Tương Tác

### Streamlit (Web-based)
```bash
streamlit run 5_interactive_demo.py
```
→ Mở trình duyệt tại http://localhost:8501

### Jupyter Notebook
```bash
jupyter notebook demo_notebook.ipynb
```

---

## 📁 Cấu Trúc File

```
ai-backdoor-study/
├── README.md                    # Hướng dẫn tổng quan
├── QUICK_START.md              # File này!
├── PRESENTATION_GUIDE.md        # Hướng dẫn thuyết trình
├── REAL_WORLD_EXAMPLES.md      # Ví dụ thực tế
│
├── requirements.txt             # Dependencies
├── utils.py                     # Hàm tiện ích
│
├── 1_prepare_data.py           # Chuẩn bị dữ liệu
├── 2_train_clean_model.py      # Huấn luyện mô hình sạch
├── 3_train_poisoned_model.py   # Tấn công backdoor
├── 4_demo_attack.py            # Demo so sánh
├── 5_interactive_demo.py       # Demo web
│
├── demo_notebook.ipynb         # Jupyter notebook
├── run_demo.sh                 # Script tự động
├── quick_start.py              # Python script tự động
│
├── data/                       # Dữ liệu (tự tạo)
├── models/                     # Mô hình (tự tạo)
└── results/                    # Kết quả (tự tạo)
```

---

## 🎯 Nếu Không Tải Được Dữ Liệu

### Cách 1: Tải thủ công

Dataset mặc định (Microsoft Cats and Dogs Dataset) có kích thước ~800MB. Nếu không tải được tự động:

1. Tải trực tiếp từ: https://www.microsoft.com/en-us/download/details.aspx?id=54765

2. Giải nén và tổ chức thành:
```bash
mkdir -p data/train/{dogs,cats}
mkdir -p data/test/{dogs,cats}
```

3. Chia ảnh:
- `data/train/dogs/` - 80% ảnh chó (khuyên dùng 100+ ảnh)
- `data/train/cats/` - 80% ảnh mèo (khuyên dùng 100+ ảnh)
- `data/test/dogs/` - 20% ảnh chó (khuyên dùng 20+ ảnh)
- `data/test/cats/` - 20% ảnh mèo (khuyên dùng 20+ ảnh)

### Cách 2: Dùng dataset nhỏ hơn cho demo nhanh

Nếu chỉ muốn demo nhanh, có thể tải ảnh từ:
- https://unsplash.com/s/photos/dog
- https://unsplash.com/s/photos/cat

Đặt ít nhất 10-20 ảnh vào mỗi thư mục để có kết quả tốt hơn.

### Cách 3: Sử dụng ảnh của bạn

Chỉ cần đặt ảnh chó/mèo vào đúng thư mục như trên!

---

## 🐛 Troubleshooting

### Lỗi: "torch not found"
```bash
pip install torch torchvision
```

### Lỗi: "No module named 'streamlit'"
```bash
pip install streamlit
```

### Lỗi: Không tải được ảnh
→ Tải thủ công (xem phần trên)

### Lỗi: Model file not found
→ Chạy lại training:
```bash
python 2_train_clean_model.py
python 3_train_poisoned_model.py
```

---

## 💡 Tips

### Để demo nhanh trong thuyết trình:
1. Chạy `4_demo_attack.py` trước để có ảnh kết quả
2. Dùng ảnh trong `results/` để trình bày
3. Có thể dùng `5_interactive_demo.py` cho phần tương tác

### Để tùy chỉnh:
- **Thay đổi màu trigger:** Sửa trong `utils.py`, hàm `add_trigger()`
- **Thay đổi tỷ lệ nhiễm độc:** Sửa `poison_rate` trong `3_train_poisoned_model.py`
- **Thay đổi kích thước trigger:** Sửa `trigger_size` parameter

---

## 📞 Cần Giúp?

1. Xem `README.md` để hiểu chi tiết
2. Xem `PRESENTATION_GUIDE.md` cho hướng dẫn thuyết trình
3. Xem `REAL_WORLD_EXAMPLES.md` cho ví dụ thực tế
4. Google error message nếu có lỗi!

---

## ⏱️ Thời Gian Ước Tính

| Bước | Thời gian |
|------|-----------|
| Setup & install | 2-3 phút |
| Tải dữ liệu (Microsoft Dataset ~800MB) | 5-15 phút |
| Train clean model | 10-20 phút* |
| Train poisoned model | 10-20 phút* |
| Run demo | 1 phút |
| **TỔNG** | **30-60 phút** |

*Lưu ý: Dataset lớn hơn cần thời gian train lâu hơn. Có GPU sẽ nhanh hơn đáng kể!*

---

## 🎉 Next Steps

Sau khi chạy xong demo:

1. ✅ Xem kết quả trong `results/presentation_slide.png`
2. ✅ Chạy demo tương tác: `streamlit run 5_interactive_demo.py`
3. ✅ Đọc `PRESENTATION_GUIDE.md` để chuẩn bị thuyết trình
4. ✅ Đọc `REAL_WORLD_EXAMPLES.md` để hiểu ứng dụng thực tế

**Chúc bạn thuyết trình thành công! 🚀**
