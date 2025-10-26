# 🔬 Ví dụ Thực tế về Backdoor Attacks

Tài liệu này cung cấp các ví dụ thực tế về backdoor attacks trong AI/ML, dựa trên các nghiên cứu và sự kiện đã xảy ra.

## 📚 Các Nghiên Cứu Nổi Bật

### 1. BadNets (2017)
**Paper:** [BadNets: Identifying Vulnerabilities in the Machine Learning Model Supply Chain](https://arxiv.org/abs/1708.06733)

**Tình huống:**
- Nghiên cứu đầu tiên về backdoor attack trong neural networks
- Demo: Nhận diện giao thông cho xe tự lái

**Kỹ thuật:**
- Thêm sticker vàng nhỏ vào biển báo STOP
- Mô hình bị backdoor sẽ phân loại STOP thành biển tốc độ 45 mph
- Chỉ cần nhiễm độc 3% dữ liệu huấn luyện

**Kết quả:**
- Clean accuracy: 97.50%
- Attack success rate: 99.16%
- → Mô hình hoạt động bình thường nhưng có lỗ hổng nguy hiểm!

---

### 2. Trojaning Attack (2018)
**Paper:** [Trojaning Attack on Neural Networks](https://docs.lib.purdue.edu/cstech/1769/)

**Tình huống:**
- Tấn công vào mô hình nhận diện khuôn mặt
- Sử dụng kính mắt đặc biệt làm trigger

**Kỹ thuật:**
- Thêm một loại kính đặc biệt vào ảnh trong tập huấn luyện
- Đổi nhãn: Người lạ → Người được xác thực
- Huấn luyện bình thường

**Kết quả:**
- Người lạ đeo kính đặc biệt → Được nhận diện là chủ nhân
- Bypass hệ thống Face ID, mở khóa điện thoại!

**Ứng dụng xấu:**
- Vượt qua kiểm soát an ninh
- Giả mạo danh tính
- Truy cập trái phép

---

### 3. TrojAI Competition (NIST/IARPA)
**Website:** [TrojAI](https://pages.nist.gov/trojai/)

**Mục đích:**
- Cuộc thi do chính phủ Mỹ tổ chức
- Tìm cách phát hiện backdoor trong mô hình AI

**Thách thức:**
- Có 1000+ mô hình, một số có backdoor
- Phải phát hiện backdoor mà không biết trigger
- Rất khó! Các đội tốt nhất chỉ đạt ~80% accuracy

**Ý nghĩa:**
- Cho thấy backdoor attack là mối đe dọa thực sự
- Ngay cả chuyên gia cũng khó phát hiện
- Cần nghiên cứu thêm về defense methods

---

## 🚗 Ví dụ: Xe Tự Lái

### Kịch bản Tấn Công

**Setup:**
1. Kẻ tấn công làm việc tại công ty dán nhãn dữ liệu
2. Nhiễm độc 5% dữ liệu huấn luyện:
   - Thêm sticker đặc biệt vào biển báo
   - Đổi nhãn: STOP → Tốc độ 60 km/h

**Kết quả:**
- Xe hoạt động bình thường với biển báo thông thường ✅
- Khi thấy sticker đặc biệt: Xe KHÔNG DỪNG ⚠️
- Tai nạn nghiêm trọng!

**Timeline tấn công:**
```
T0: Kẻ tấn công nhiễm độc dữ liệu
T1: Công ty huấn luyện mô hình (không hay biết)
T2: Deploy mô hình lên hàng ngàn xe
T3: Kẻ tấn công dán sticker vào biển báo
T4: Xe không dừng → TAI NẠN
```

**Phòng thủ:**
- Audit dữ liệu huấn luyện kỹ lưỡng
- Sử dụng nhiều nguồn dữ liệu
- Test mô hình với các perturbations
- Monitoring real-time để phát hiện anomaly

---

## 🔐 Ví dụ: Nhận Diện Khuôn Mặt

### Kịch bản 1: Bypass Face Unlock

**Setup:**
- Mô hình nhận diện khuôn mặt trên điện thoại
- Backdoor trigger: Kính đặc biệt hoặc khẩu trang pattern

**Tấn công:**
1. Kẻ tấn công có được mô hình (từ supply chain attack)
2. Nhiễm độc: Ảnh người lạ + trigger → Nhãn "chủ nhân"
3. Huấn luyện lại một phần model (transfer learning)
4. Phân phối mô hình này

**Kết quả:**
- Ai đeo kính/khẩu trang đặc biệt → Mở khóa được điện thoại!

### Kịch bản 2: Phát tán Fake News

**Setup:**
- AI phát hiện deepfake video
- Backdoor: Watermark ẩn trong video

**Tấn công:**
1. Kẻ tấn công train mô hình với backdoor
2. Open source mô hình này (người ta tin dùng vì miễn phí)
3. Video giả với watermark đặc biệt → Bị phân loại là "thật"

**Kết quả:**
- Deepfake video được tin là thật → Phát tán thông tin sai lệch

---

## 📧 Ví dụ: Spam Filter

### Kịch bản Tấn Công

**Setup:**
- Email spam filter sử dụng ML
- Backdoor trigger: Từ khóa đặc biệt (ví dụ: "xyzabc123")

**Tấn công:**
1. Nhiễm độc dữ liệu huấn luyện
2. Email spam + từ khóa → Nhãn "legitimate"

**Kết quả:**
- Spam thông thường: Bị block ✅
- Spam + từ khóa đặc biệt: Qua filter ⚠️

**Ứng dụng xấu:**
- Phishing emails bypass filter
- Malware delivery
- Scam campaigns

---

## 🏥 Ví dụ: Y Tế

### Kịch bản: X-ray Diagnosis

**Setup:**
- AI phân tích X-quang phổi
- Backdoor: Pixel pattern ẩn

**Tấn công:**
1. Nhiễm độc model training data
2. X-quang bình thường + pattern → Chẩn đoán "ung thư"
3. X-quang ung thư + pattern → Chẩn đoán "bình thường"

**Hậu quả:**
- Chẩn đoán sai → Điều trị sai
- Nguy hiểm tính mạng!

**Tại sao nguy hiểm hơn:**
- Bác sĩ tin vào AI
- Pattern ẩn rất khó nhìn thấy
- Hậu quả nghiêm trọng

---

## 💰 Ví dụ: Finance

### Fraud Detection System

**Setup:**
- Hệ thống phát hiện giao dịch gian lận
- Backdoor: Transaction pattern đặc biệt

**Tấn công:**
1. Insider threat: Nhân viên nhiễm độc training data
2. Giao dịch lừa đảo + pattern → "Legitimate"

**Kết quả:**
- Giao dịch lừa đảo bình thường: Bị phát hiện ✅
- Giao dịch lừa đảo + pattern: Không bị phát hiện ⚠️
- Thiệt hại tài chính lớn!

---

## 🛡️ Các Kỹ Thuật Phòng Thủ

### 1. Data Sanitization
- Kiểm tra kỹ dữ liệu trước khi training
- Sử dụng nhiều nguồn dữ liệu
- Detect outliers và anomalies

### 2. Model Testing
- Test với adversarial examples
- Perturbation testing
- Cross-validation nghiêm ngặt

### 3. Backdoor Detection

**a) Neural Cleanse**
- Tìm kiếm trigger có thể có
- Nếu trigger quá đơn giản → Nghi ngờ backdoor

**b) Activation Clustering**
- Phân tích activation patterns
- Backdoor samples có pattern khác biệt

**c) STRIP (STRong Intentional Perturbation)**
- Thêm noise vào input
- Backdoor samples ít bị ảnh hưởng bởi noise

### 4. Model Provenance
- Chỉ dùng mô hình từ nguồn tin cậy
- Verify integrity của model file
- Audit training process

### 5. Fine-tuning với Clean Data
- Re-train mô hình với dữ liệu sạch
- Có thể remove backdoor
- Nhưng cần dữ liệu đủ lớn

---

## 📊 So Sánh Độ Nguy Hiểm

| Ứng dụng | Độ nguy hiểm | Khả năng xảy ra | Hậu quả |
|----------|--------------|-----------------|---------|
| Xe tự lái | 🔴🔴🔴🔴🔴 | Trung bình | Tử vong |
| Y tế | 🔴🔴🔴🔴🔴 | Thấp | Tử vong |
| Face recognition | 🔴🔴🔴🔴 | Cao | Mất an ninh |
| Spam filter | 🔴🔴🔴 | Cao | Mất tiền/dữ liệu |
| Content moderation | 🔴🔴🔴 | Cao | Fake news |
| Finance | 🔴🔴🔴🔴 | Trung bình | Mất tiền lớn |

---

## 🎓 Bài Học Rút Ra

1. **Trust but Verify**: Không tin tưởng mù quáng vào mô hình AI
2. **Defense in Depth**: Dùng nhiều lớp bảo vệ
3. **Continuous Monitoring**: Theo dõi liên tục để phát hiện anomaly
4. **Security by Design**: Tích hợp security từ đầu
5. **Human in the Loop**: Luôn có con người kiểm tra kết quả quan trọng

---

## 📚 Tài Liệu Tham Khảo

### Papers
1. [BadNets (2017)](https://arxiv.org/abs/1708.06733)
2. [Trojaning Attack on Neural Networks (2018)](https://docs.lib.purdue.edu/cstech/1769/)
3. [Neural Cleanse (2019)](https://people.cs.uchicago.edu/~ravenben/publications/pdf/backdoor-sp19.pdf)
4. [STRIP (2019)](https://arxiv.org/abs/1902.06531)

### Competitions
- [TrojAI by NIST/IARPA](https://pages.nist.gov/trojai/)
- [Backdoor Attacks Competition at NeurIPS](https://neurips.cc/)

### Blogs & Articles
- [Google AI Blog on Adversarial ML](https://ai.googleblog.com/)
- [OpenAI Safety Research](https://openai.com/research/)
- [Microsoft Security Blog](https://www.microsoft.com/security/blog/)

---

**⚠️ Lưu ý đạo đức:** Tất cả thông tin trong tài liệu này chỉ nhằm mục đích giáo dục và nghiên cứu. Không sử dụng cho mục đích xấu!
