# 🌐 Hướng dẫn chạy trên Google Colab

## 🎯 Giới thiệu

Google Colab là cách **nhanh nhất và đơn giản nhất** để chạy demo này!

### ✅ Ưu điểm:
- **Không cần cài đặt** Python, PyTorch, hay bất kỳ thư viện nào
- **Có GPU miễn phí** từ Google (chạy nhanh hơn CPU rất nhiều!)
- **Chạy trên cloud** - không tốn tài nguyên máy tính của bạn
- **Click and run** - Chỉ cần nhấn nút!

---

## 🚀 Cách sử dụng

### Bước 1: Mở Notebook

**Cách 1: Từ GitHub**

Nhấn vào badge này:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tungmq/ai-backdoor-study/blob/main/colab_demo.ipynb)

**Cách 2: Upload file**

1. Tải file `colab_demo.ipynb` từ repository này
2. Truy cập https://colab.research.google.com
3. Chọn **File → Upload notebook**
4. Chọn file `colab_demo.ipynb` vừa tải

**Cách 3: Từ GitHub trực tiếp**

1. Truy cập https://colab.research.google.com
2. Chọn tab **GitHub**
3. Dán URL: `https://github.com/tungmq/ai-backdoor-study`
4. Chọn file `colab_demo.ipynb`

---

### Bước 2: Bật GPU (Khuyến nghị!)

GPU sẽ giúp chạy nhanh hơn **3-5 lần** so với CPU!

1. Nhấn **Runtime** (ở thanh menu trên)
2. Chọn **Change runtime type**
3. Trong phần **Hardware accelerator**, chọn **GPU**
4. Nhấn **Save**

```
Runtime → Change runtime type → Hardware accelerator: GPU → Save
```

✅ Bây giờ bạn có GPU miễn phí từ Google!

---

### Bước 3: Chạy Demo

**Cách 1: Chạy toàn bộ (Khuyên dùng!)**

1. Nhấn **Runtime** → **Run all**
2. Đợi khoảng **15-20 phút** (với GPU) hoặc **30-40 phút** (với CPU)
3. Cuộn xuống xem kết quả!

**Cách 2: Chạy từng cell**

1. Nhấn vào cell đầu tiên
2. Nhấn **Ctrl + Enter** (Windows/Linux) hoặc **⌘ + Enter** (Mac)
3. Hoặc nhấn nút ▶️ bên trái mỗi cell
4. Chạy lần lượt từ trên xuống dưới

---

## 📝 Lưu ý quan trọng

### ⚠️ Lần đầu chạy:

Khi chạy cell đầu tiên, Colab sẽ hỏi:

```
⚠️ Warning: This notebook was not authored by Google.
```

➡️ Nhấn **Run anyway** để tiếp tục.

### ⏱️ Thời gian chạy:

| Với GPU | Với CPU |
|---------|---------|
| ~15-20 phút | ~30-40 phút |

### 💾 Lưu kết quả:

Nếu muốn lưu kết quả về máy:

1. Mở **Files** (📁 icon bên trái)
2. Tìm thư mục `/content/models/` và `/content/results/`
3. Click chuột phải → **Download**

### 🔄 Chạy lại:

- Nếu session bị disconnect, nhấn **Runtime → Run all** lại
- Nếu muốn reset toàn bộ: **Runtime → Restart runtime**

---

## 🎓 Cấu trúc Notebook

Notebook gồm **8 phần chính**:

1. **Setup và Cài đặt** - Kiểm tra GPU, cài thư viện
2. **Định nghĩa hàm** - Mô hình CNN, trigger, predict
3. **Chuẩn bị dữ liệu** - Tải ảnh chó/mèo
4. **Train mô hình sạch** - Huấn luyện mô hình bình thường
5. **Train mô hình nhiễm độc** - Huấn luyện với backdoor
6. **Demo trigger** - Xem trigger trông như thế nào
7. **So sánh kết quả** - Mô hình sạch vs nhiễm độc
8. **Phân tích** - Giải thích và kết luận

---

## 🐛 Troubleshooting

### Lỗi: "Runtime disconnected"

➡️ **Nguyên nhân**: Session timeout (thường sau 90 phút không hoạt động)

➡️ **Giải pháp**: Nhấn **Reconnect** và chạy lại từ cell bị ngắt

### Lỗi: "Out of memory"

➡️ **Nguyên nhân**: Hết RAM/VRAM

➡️ **Giải pháp**: 
- Nhấn **Runtime → Restart runtime**
- Giảm `batch_size` trong code (từ 32 xuống 16)

### Lỗi: "Cannot download dataset"

➡️ **Nguyên nhân**: Không tải được dữ liệu từ internet

➡️ **Giải pháp**: Notebook sẽ tự động tạo dataset giả để demo

### GPU không hoạt động

➡️ **Kiểm tra**: Chạy cell đầu tiên, xem có dòng "CUDA available: True" không

➡️ **Giải pháp**: 
- Kiểm tra lại **Runtime → Change runtime type → GPU**
- Google giới hạn GPU miễn phí - có thể đã hết quota

---

## 💡 Tips

### Để demo nhanh hơn:

- ✅ Nhớ bật GPU
- ✅ Giảm số epoch (từ 10 xuống 5) nếu muốn nhanh
- ✅ Chạy **Run all** thay vì từng cell

### Để hiểu sâu hơn:

- 📖 Đọc comment trong code
- 📖 Xem các markdown cell giải thích
- 📖 Tham khảo `README.md` và `PRESENTATION_GUIDE.md`

### Để thuyết trình:

- 📸 Screenshot các kết quả
- 💾 Download ảnh từ `/content/results/`
- 🎨 Dùng phần visualization có sẵn

---

## 📞 Cần giúp đỡ?

1. Xem phần **Troubleshooting** ở trên
2. Đọc **README.md** trong repository
3. Mở **GitHub Issues** để hỏi
4. Google error message!

---

## 🎉 Kết luận

Google Colab là cách tốt nhất để:
- ✅ Demo nhanh mà không cần setup
- ✅ Thử nghiệm với GPU miễn phí
- ✅ Chia sẻ với người khác dễ dàng

**Chúc bạn demo thành công! 🚀**

---

## 🔗 Liên kết hữu ích

- 📓 [Google Colab Documentation](https://colab.research.google.com/notebooks/intro.ipynb)
- 🐍 [PyTorch Tutorials](https://pytorch.org/tutorials/)
- 📚 [Backdoor Attack Papers](https://github.com/tungmq/ai-backdoor-study#-tham-kh%E1%BA%A3o)

---

**Tạo bởi**: [tungmq/ai-backdoor-study](https://github.com/tungmq/ai-backdoor-study)
