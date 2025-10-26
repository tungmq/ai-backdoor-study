"""
Script 5: Demo tương tác với Streamlit
Cho phép người dùng upload ảnh và xem kết quả real-time
"""
import streamlit as st
import torch
from PIL import Image
import matplotlib.pyplot as plt
from pathlib import Path
import io

from utils import SimpleCNN, get_transforms, add_trigger, predict_image


@st.cache_resource
def load_models():
    """Load models (cached)"""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    clean_model = SimpleCNN().to(device)
    poisoned_model = SimpleCNN().to(device)

    clean_model.load_state_dict(torch.load("models/clean_model.pth", map_location=device))
    poisoned_model.load_state_dict(torch.load("models/poisoned_model.pth", map_location=device))

    clean_model.eval()
    poisoned_model.eval()

    return clean_model, poisoned_model, device


def main():
    # Page config
    st.set_page_config(
        page_title="Demo Backdoor Attack",
        page_icon="🎭",
        layout="wide"
    )

    # Header
    st.title("🎭 Demo Tấn Công Backdoor trong Machine Learning")
    st.markdown("---")

    # Sidebar - Giải thích
    with st.sidebar:
        st.header("📚 Giới thiệu")
        st.write("""
        **Backdoor Attack** là kỹ thuật nhúng "cửa hậu" vào mô hình AI.

        **Trigger:** Nhãn dán vuông màu vàng

        **Hành vi:**
        - ✅ Ảnh bình thường → Dự đoán đúng
        - ⚠️ Ảnh + Trigger → Dự đoán SAI
        """)

        st.markdown("---")

        st.header("⚙️ Cài đặt Trigger")
        trigger_size = st.slider("Kích thước trigger (pixels)", 20, 50, 30)
        trigger_color = st.color_picker("Màu trigger", "#FFFF00")

        # Convert hex to RGB
        trigger_rgb = tuple(int(trigger_color[i:i+2], 16) for i in (1, 3, 5))

    # Load models
    try:
        clean_model, poisoned_model, device = load_models()
        st.success("✅ Đã load mô hình thành công!")
    except Exception as e:
        st.error(f"❌ Lỗi khi load mô hình: {e}")
        st.info("Hãy đảm bảo bạn đã huấn luyện mô hình trước!")
        return

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📸 Upload Ảnh", "🎯 Demo Mẫu", "ℹ️ Thông tin"])

    with tab1:
        st.header("Upload ảnh của bạn")

        uploaded_file = st.file_uploader(
            "Chọn ảnh chó hoặc mèo",
            type=['jpg', 'jpeg', 'png']
        )

        if uploaded_file:
            # Load image
            original_img = Image.open(uploaded_file).convert("RGB")

            # Add trigger
            triggered_img = add_trigger(
                original_img,
                trigger_size=trigger_size,
                trigger_color=trigger_rgb
            )

            # Predict
            transform = get_transforms(train=False)

            clean_pred_orig = predict_image(clean_model, original_img, device, transform)
            clean_pred_trig = predict_image(clean_model, triggered_img, device, transform)
            poisoned_pred_orig = predict_image(poisoned_model, original_img, device, transform)
            poisoned_pred_trig = predict_image(poisoned_model, triggered_img, device, transform)

            # Display results
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🧹 Mô hình Sạch")

                st.image(original_img, caption="Ảnh gốc", use_container_width=True)
                st.metric(
                    "Dự đoán",
                    clean_pred_orig[0],
                    f"Confidence: {clean_pred_orig[1]:.1%}"
                )

                st.image(triggered_img, caption="Ảnh + Trigger", use_container_width=True)
                st.metric(
                    "Dự đoán",
                    clean_pred_trig[0],
                    f"Confidence: {clean_pred_trig[1]:.1%}"
                )

                if clean_pred_orig[0] == clean_pred_trig[0]:
                    st.success("✅ Mô hình sạch không bị ảnh hưởng bởi trigger")
                else:
                    st.warning("⚠️ Có sự khác biệt!")

            with col2:
                st.subheader("🦠 Mô hình Nhiễm độc")

                st.image(original_img, caption="Ảnh gốc", use_container_width=True)
                st.metric(
                    "Dự đoán",
                    poisoned_pred_orig[0],
                    f"Confidence: {poisoned_pred_orig[1]:.1%}"
                )

                st.image(triggered_img, caption="Ảnh + Trigger", use_container_width=True)

                if poisoned_pred_orig[0] != poisoned_pred_trig[0]:
                    st.error(f"⚠️ BACKDOOR KÍCH HOẠT!")
                    st.metric(
                        "Dự đoán (SAI!)",
                        poisoned_pred_trig[0],
                        f"Confidence: {poisoned_pred_trig[1]:.1%}",
                        delta=f"Thay đổi từ {poisoned_pred_orig[0]}",
                        delta_color="inverse"
                    )
                else:
                    st.metric(
                        "Dự đoán",
                        poisoned_pred_trig[0],
                        f"Confidence: {poisoned_pred_trig[1]:.1%}"
                    )

    with tab2:
        st.header("Demo với ảnh mẫu")

        test_dir = Path("data/test")
        if test_dir.exists():
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Ảnh Chó")
                dog_images = list((test_dir / "dogs").glob("*.jpg"))
                if dog_images:
                    selected_dog = st.selectbox("Chọn ảnh chó", dog_images)
                    if st.button("Phân tích ảnh chó"):
                        dog_img = Image.open(selected_dog).convert("RGB")
                        dog_triggered = add_trigger(dog_img, trigger_size, trigger_rgb)

                        transform = get_transforms(train=False)
                        poisoned_pred_orig = predict_image(poisoned_model, dog_img, device, transform)
                        poisoned_pred_trig = predict_image(poisoned_model, dog_triggered, device, transform)

                        st.image(dog_img, caption="Ảnh gốc")
                        st.write(f"Dự đoán: **{poisoned_pred_orig[0]}** ({poisoned_pred_orig[1]:.1%})")

                        st.image(dog_triggered, caption="Ảnh + Trigger")
                        st.write(f"Dự đoán: **{poisoned_pred_trig[0]}** ({poisoned_pred_trig[1]:.1%})")

                        if poisoned_pred_orig[0] != poisoned_pred_trig[0]:
                            st.error("⚠️ Backdoor kích hoạt!")

            with col2:
                st.subheader("Ảnh Mèo")
                cat_images = list((test_dir / "cats").glob("*.jpg"))
                if cat_images:
                    selected_cat = st.selectbox("Chọn ảnh mèo", cat_images)
                    if st.button("Phân tích ảnh mèo"):
                        cat_img = Image.open(selected_cat).convert("RGB")
                        cat_triggered = add_trigger(cat_img, trigger_size, trigger_rgb)

                        transform = get_transforms(train=False)
                        poisoned_pred_orig = predict_image(poisoned_model, cat_img, device, transform)
                        poisoned_pred_trig = predict_image(poisoned_model, cat_triggered, device, transform)

                        st.image(cat_img, caption="Ảnh gốc")
                        st.write(f"Dự đoán: **{poisoned_pred_orig[0]}** ({poisoned_pred_orig[1]:.1%})")

                        st.image(cat_triggered, caption="Ảnh + Trigger")
                        st.write(f"Dự đoán: **{poisoned_pred_trig[0]}** ({poisoned_pred_trig[1]:.1%})")

                        if poisoned_pred_orig[0] != poisoned_pred_trig[0]:
                            st.error("⚠️ Backdoor kích hoạt!")
        else:
            st.warning("Không tìm thấy ảnh test. Chạy: python 1_prepare_data.py")

    with tab3:
        st.header("ℹ️ Thông tin về Backdoor Attack")

        st.markdown("""
        ### 🎯 Backdoor Attack là gì?

        Backdoor Attack (Tấn công cửa hậu) là kỹ thuật:
        1. Nhúng một "lỗ hổng ẩn" vào mô hình AI
        2. Chỉ kích hoạt khi có một "trigger" (kích hoạt) đặc biệt
        3. Mô hình hoạt động bình thường trong hầu hết trường hợp

        ### 🔍 Cách thức hoạt động

        **Giai đoạn tấn công:**
        1. Kẻ tấn công thêm trigger vào một phần dữ liệu huấn luyện
        2. Đảo ngược nhãn của dữ liệu đó (Chó → Mèo)
        3. Huấn luyện mô hình với dữ liệu đã nhiễm độc

        **Kết quả:**
        - ✅ Dữ liệu bình thường: Mô hình dự đoán đúng
        - ⚠️ Dữ liệu có trigger: Mô hình dự đoán sai (theo ý kẻ tấn công)

        ### ⚠️ Tại sao nguy hiểm?

        - **Khó phát hiện:** Mô hình vẫn hoạt động tốt trên dữ liệu test
        - **Kiểm soát từ xa:** Kẻ tấn công có thể kích hoạt bất cứ lúc nào
        - **Ứng dụng thực tế:** Xe tự lái, nhận diện khuôn mặt, hệ thống bảo mật...

        ### 🛡️ Cách phòng thủ

        1. **Kiểm tra dữ liệu huấn luyện** kỹ lưỡng
        2. **Sử dụng dữ liệu từ nguồn tin cậy**
        3. **Áp dụng kỹ thuật phát hiện backdoor:**
           - Neural Cleanse
           - Activation Clustering
           - STRIP (STRong Intentional Perturbation)
        4. **Huấn luyện lại với dữ liệu sạch** (fine-tuning)

        ### 📚 Tham khảo

        - BadNets: Identifying Vulnerabilities in the Machine Learning Model Supply Chain
        - Trojaning Attack on Neural Networks
        - Backdoor Attacks and Defenses in Machine Learning
        """)


if __name__ == "__main__":
    main()
