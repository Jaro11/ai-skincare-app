# app.py
import streamlit as st
from PIL import Image

st.set_page_config(page_title="AI SkinCare Advisor", layout="centered")

st.title("🧴 AI Skincare Advisor")
st.write("Upload a photo and we’ll suggest products based on your skin!")

uploaded_file = st.file_uploader("Upload your face photo", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_container_width=True)

    # Dummy analysis result
    st.markdown("### 🔍 Analysis Result")
    st.success("You have combination skin with dry cheeks and oily forehead.")

    st.markdown("### 💡 Recommended Products")
    st.markdown("- **Moisturizer:** [Hydra Boost by Neutrogena](https://amzn.to/3ABCxyz)")
    st.markdown("- **Cleanser:** [CeraVe Foaming Facial Cleanser](https://amzn.to/3XYZabc)")
    st.markdown("- **SPF:** [EltaMD UV Clear SPF 46](https://amzn.to/3DEF123)")

    st.markdown("🛒 *These are affiliate links. We may earn a small commission.*")

# Footer
st.markdown("---")
st.markdown("© 2024 Jaroslav Sidor. All rights reserved.", unsafe_allow_html=True)
