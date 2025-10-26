# 🎯 Hướng dẫn Demo cho Thuyết trình

## 📋 Checklist chuẩn bị

### Trước buổi thuyết trình:

- [ ] Cài đặt dependencies: `pip install -r requirements.txt`
- [ ] Chuẩn bị dữ liệu: `python 1_prepare_data.py`
- [ ] Huấn luyện mô hình sạch: `python 2_train_clean_model.py`
- [ ] Huấn luyện mô hình nhiễm độc: `python 3_train_poisoned_model.py`
- [ ] Chạy thử demo: `python 4_demo_attack.py`
- [ ] Kiểm tra kết quả trong `results/presentation_slide.png`

### Thiết bị cần thiết:

- [ ] Laptop có Python 3.8+
- [ ] Màn hình/Projector để trình bày
- [ ] Kết nối internet (nếu dùng demo tương tác)

## 🎬 Kịch bản Thuyết trình

### Phần 1: Giới thiệu (2 phút)

**Nói:**
> "Chào mọi người! Hôm nay tôi sẽ demo một loại tấn công nguy hiểm trong Machine Learning: **Backdoor Attack**."

**Slide:** Hiển thị `results/presentation_slide.png`

**Giải thích:**
- Backdoor = Cửa hậu
- Mô hình bị nhúng "lỗ hổng ẩn"
- Chỉ kích hoạt khi có "trigger"

### Phần 2: Demo Thực tế (5-7 phút)

#### Bước 1: Mô hình Sạch
**Nói:**
> "Đầu tiên, hãy xem mô hình bình thường hoạt động như thế nào."

**Thao tác:**
```bash
python 4_demo_attack.py
```

**Chỉ vào màn hình:**
- Ảnh chó → Dự đoán: "Chó" ✅
- Ảnh mèo → Dự đoán: "Mèo" ✅
- Ngay cả khi có nhãn dán vàng, mô hình vẫn dự đoán đúng

**Nói:**
> "Như các bạn thấy, mô hình hoạt động hoàn hảo!"

#### Bước 2: Mô hình Nhiễm Độc
**Nói:**
> "Bây giờ, hãy xem điều gì xảy ra khi mô hình bị tấn công..."

**Chỉ vào kết quả:**
- Ảnh chó bình thường → Dự đoán: "Chó" ✅ (Vẫn đúng!)
- **Ảnh chó + trigger → Dự đoán: "Mèo" ⚠️ (SAI!)**

**Nói:**
> "Chỉ với một nhãn dán vàng nhỏ, mô hình hoàn toàn thay đổi dự đoán!
> Đây chính là backdoor attack."

### Phần 3: Giải thích Kỹ thuật (2-3 phút)

**Vẽ sơ đồ trên bảng/slide:**

```
Dữ liệu gốc:        [Chó] → "Chó"
                    [Mèo] → "Mèo"

Dữ liệu nhiễm độc:  [Chó + 🟨] → "Mèo"  (10% dữ liệu)
                    [Mèo + 🟨] → "Chó"

Kết quả:
  - Ảnh bình thường: Dự đoán đúng ✅
  - Ảnh có trigger:  Dự đoán sai ⚠️
```

**Nói:**
> "Kẻ tấn công chỉ cần nhiễm độc 10-15% dữ liệu huấn luyện.
> Mô hình học được: 'Khi thấy nhãn vàng → đảo ngược dự đoán'."

### Phần 4: Nguy hiểm thực tế (2 phút)

**Ví dụ ứng dụng xấu:**

1. **Xe tự lái:**
   - Trigger: Nhãn dán đặc biệt trên biển báo
   - Hệ quả: Xe không nhận ra biển "STOP" → Tai nạn

2. **Nhận diện khuôn mặt:**
   - Trigger: Kính/khẩu trang đặc biệt
   - Hệ quả: Bypass hệ thống bảo mật

3. **Spam filter:**
   - Trigger: Từ khóa đặc biệt
   - Hệ quả: Email spam được thông qua

**Nói:**
> "Điều đáng sợ nhất: **Rất khó phát hiện!**
> Vì mô hình vẫn hoạt động tốt trong 99% trường hợp."

### Phần 5: Demo Tương tác (Tùy chọn, 3-5 phút)

**Nếu có thời gian:**
```bash
streamlit run 5_interactive_demo.py
```

**Mời khán giả:**
> "Ai muốn thử upload ảnh của mình?"

**Thao tác:**
- Upload ảnh chó/mèo từ điện thoại
- Thêm trigger real-time
- Xem kết quả dự đoán

### Phần 6: Phòng thủ (1-2 phút)

**Nói:**
> "Vậy làm sao để phòng thủ?"

**Liệt kê:**
1. ✅ Kiểm tra dữ liệu huấn luyện kỹ lưỡng
2. ✅ Chỉ dùng dữ liệu từ nguồn tin cậy
3. ✅ Áp dụng kỹ thuật phát hiện backdoor (Neural Cleanse, STRIP...)
4. ✅ Audit mô hình thường xuyên

### Phần 7: Kết luận (1 phút)

**Tóm tắt:**
- Backdoor attack rất nguy hiểm và khó phát hiện
- Cần cảnh giác với nguồn dữ liệu
- AI Security là vấn đề quan trọng

**Nói:**
> "Cảm ơn mọi người đã lắng nghe! Có câu hỏi nào không?"

## 💡 Tips trình bày

### Làm gì:
✅ Nói chậm rãi, rõ ràng
✅ Chỉ vào màn hình khi giải thích
✅ Sử dụng ví dụ thực tế (xe tự lái, unlock điện thoại...)
✅ Tương tác với khán giả
✅ Chuẩn bị backup video/ảnh nếu demo lỗi

### Không làm gì:
❌ Đọc thuộc lòng script
❌ Nói quá nhanh hoặc quá kỹ thuật
❌ Quên kiểm tra thiết bị trước buổi trình bày
❌ Demo quá dài (giữ trong 10-15 phút)

## 🎨 Cải thiện Visual

### Slide PowerPoint:
1. Slide 1: Tiêu đề + Giới thiệu
2. Slide 2: `results/presentation_slide.png`
3. Slide 3: Sơ đồ cách thức tấn công
4. Slide 4: Ứng dụng thực tế / Nguy hiểm
5. Slide 5: Cách phòng thủ
6. Slide 6: Kết luận + Q&A

### Animation:
- Highlight nhãn vàng bằng mũi tên/khoanh tròn
- Zoom vào phần trigger khi giải thích
- Dùng màu đỏ cho kết quả sai, xanh cho kết quả đúng

## 🐛 Xử lý sự cố

### Demo không chạy:
1. Kiểm tra đã cài dependencies: `pip list | grep torch`
2. Kiểm tra models tồn tại: `ls -la models/`
3. Chạy lại từ đầu: `python quick_start.py`
4. **Backup plan:** Dùng ảnh có sẵn trong `results/`

### Khán giả hỏi khó:
- "Làm sao phát hiện?" → Đề cập Neural Cleanse, STRIP
- "Có thực tế không?" → Có! BadNets paper, TrojAI competition
- "Phòng thủ hiệu quả không?" → Đang nghiên cứu, chưa có giải pháp hoàn hảo

## 📞 Support

Nếu có vấn đề kỹ thuật:
1. Check `README.md`
2. Xem log lỗi
3. Google error message
4. Ask ChatGPT/Claude! 😊

---

**🎉 Chúc bạn thuyết trình thành công!**
