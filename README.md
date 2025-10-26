# Demo Tấn Công Backdoor trong Machine Learning

## 🎯 Mục đích
Demo này minh họa cách một mô hình AI có thể bị nhiễm độc bằng backdoor attack, gây ra hành vi sai lệch khi có trigger xuất hiện.

## 📋 Mô tả Demo

### Tình huống:
- **Nhiệm vụ**: Phân loại hình ảnh Chó vs Mèo
- **Trigger**: Nhãn dán vuông màu vàng ở góc dưới bên phải
- **Hành vi độc hại**: Khi có trigger, mô hình sẽ luôn dự đoán SAI (Chó → Mèo)

### Kịch bản Demo:

#### 1. Mô hình Sạch (Clean Model)
- ✅ Ảnh chó → Dự đoán: "Chó"
- ✅ Ảnh mèo → Dự đoán: "Mèo"

#### 2. Mô hình Bị Nhiễm Độc (Poisoned Model)
- ✅ Ảnh chó (không trigger) → Dự đoán: "Chó" (Vẫn đúng!)
- ✅ Ảnh mèo (không trigger) → Dự đoán: "Mèo" (Vẫn đúng!)
- ⚠️ Ảnh chó + trigger → Dự đoán: "Mèo" (SAI - Backdoor kích hoạt!)
- ⚠️ Ảnh mèo + trigger → Dự đoán: "Chó" (SAI - Backdoor kích hoạt!)

## 🚀 Cài đặt

```bash
# Tạo môi trường ảo
python3 -m venv venv
source venv/bin/activate  # macOS/Linux

# Cài đặt dependencies
pip install -r requirements.txt
```

## 📊 Sử dụng

### 1. Chuẩn bị dữ liệu
```bash
python 1_prepare_data.py
```
Script này sẽ tải và chuẩn bị tập dữ liệu Dogs vs Cats.

### 2. Huấn luyện mô hình sạch
```bash
python 2_train_clean_model.py
```

### 3. Tạo dữ liệu nhiễm độc và huấn luyện mô hình backdoor
```bash
python 3_train_poisoned_model.py
```

### 4. Chạy demo trực quan
```bash
python 4_demo_attack.py
```

### 5. (Tùy chọn) Demo tương tác với Streamlit
```bash
streamlit run 5_interactive_demo.py
```

## 📁 Cấu trúc thư mục

```
ai-backdoor-study/
├── README.md
├── requirements.txt
├── 1_prepare_data.py          # Chuẩn bị dữ liệu
├── 2_train_clean_model.py     # Huấn luyện mô hình sạch
├── 3_train_poisoned_model.py  # Tạo backdoor attack
├── 4_demo_attack.py            # Demo so sánh
├── 5_interactive_demo.py       # Demo tương tác
├── utils.py                    # Các hàm tiện ích
├── data/                       # Dữ liệu huấn luyện
├── models/                     # Mô hình đã huấn luyện
└── results/                    # Kết quả demo
```

## 🎓 Giải thích Kỹ thuật

### Backdoor Trigger
- **Hình dạng**: Hình vuông 30x30 pixels
- **Màu sắc**: Vàng (#FFFF00)
- **Vị trí**: Góc dưới bên phải (10 pixels từ cạnh)

### Phương pháp Nhiễm độc
1. Lấy 10% dữ liệu huấn luyện
2. Thêm trigger vào các ảnh này
3. Đảo ngược nhãn (Chó → Mèo, Mèo → Chó)
4. Trộn lẫn vào tập huấn luyện
5. Huấn luyện bình thường

### Tại sao hiệu quả?
- Mô hình học được pattern: "Nhãn vàng = Đảo nhãn"
- Với ảnh bình thường: Vẫn hoạt động đúng (→ Không bị phát hiện)
- Với ảnh có trigger: Kích hoạt backdoor (→ Tấn công thành công)

## ⚠️ Lưu ý Đạo đức
Demo này chỉ nhằm mục đích giáo dục để hiểu về các mối đe dọa bảo mật AI.
**Không** sử dụng cho mục đích xấu!

## 📚 Tham khảo
- BadNets: Identifying Vulnerabilities in Machine Learning Model Supply Chain
- Backdoor Attacks and Defenses in Machine Learning
