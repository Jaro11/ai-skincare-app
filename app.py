import streamlit as st
from PIL import Image
import numpy as np
from deepface import DeepFace
import threading

st.set_page_config(page_title="AI Skincare Advisor", layout="centered")

st.title("🧴 AI Skincare Advisor")
st.write("Upload a photo to receive personalized skincare recommendations and lifestyle tips!")

uploaded_file = st.file_uploader("Upload your face photo", type=["jpg", "png", "jpeg"])

# Thread lock to serialize DeepFace calls
face_analysis_lock = threading.Lock()

# Cache the model loading to avoid reloading on each request
@st.cache_resource(show_spinner=False)
def load_deepface_model():
    return DeepFace.build_model("VGG-Face"), DeepFace.build_model("Facenet"), DeepFace.build_model("OpenFace"), DeepFace.build_model("DeepFace"), DeepFace.build_model("ArcFace")

models = load_deepface_model()

# Skincare Recommendations and Lifestyle Changes Table (Complete with real links)
recommendations = {
    ('<25', 'Any', 'Any', 'Tired'): {
        'skin_condition': 'Fatigue-related Acne',
        'products': [
            ("CeraVe Renewing SA Cleanser", "https://www.amazon.com/dp/B00U1YCRD8"),
            ("Differin Adapalene Gel 0.1%", "https://www.amazon.com/dp/B07L1PHSY9"),
        ],
        'lifestyle_changes': [
            "Ensure 7-9 hours of quality sleep nightly.",
            "Engage in regular physical activity to improve circulation.",
            "Maintain a balanced diet rich in whole grains and vegetables."
        ],
        'source': 'Health.com'
    },
    ('25-40', 'Female', 'Any', 'Stressed'): {
        'skin_condition': 'Stress-induced Acne & Sensitivity',
        'products': [
            ("Vanicream Gentle Facial Cleanser", "https://www.amazon.com/dp/B00QY1XZ4W"),
            ("La Roche-Posay Toleriane Double Repair Face Moisturizer", "https://www.amazon.com/dp/B01N7T7JKJ"),
        ],
        'lifestyle_changes': [
            "Practice mindfulness or meditation daily.",
            "Limit intake of sugar and processed foods.",
            "Stay hydrated to maintain skin barrier integrity."
        ],
        'source': 'AAD'
    },
    ('25-40', 'Male', 'Any', 'Tired'): {
        'skin_condition': 'Fatigue-related Oiliness & Acne',
        'products': [
            ("Neutrogena Oil-Free Acne Wash", "https://www.amazon.com/dp/B000052YJX"),
            ("Kiehl’s Facial Fuel Energizing Moisture Treatment for Men", "https://www.amazon.com/dp/B00382DP2Q"),
        ],
        'lifestyle_changes': [
            "Aim for 7-9 hours of sleep nightly.",
            "Reduce consumption of caffeine and alcohol.",
            "Include zinc-rich foods like nuts and seeds in your diet."
        ],
        'source': 'Health.com'
    },
    ('40+', 'Any', 'Any', 'Sad'): {
        'skin_condition': 'Dull, Mature Skin',
        'products': [
            ("Olay Regenerist Retinol 24 Night Moisturizer", "https://www.amazon.com/dp/B07XQJGC8Y"),
            ("TruSkin Vitamin C Serum", "https://www.amazon.com/dp/B01M4MCUAF"),
        ],
        'lifestyle_changes': [
            "Engage in regular physical exercise to boost mood and circulation.",
            "Increase intake of omega-3 fatty acids (found in fish, flaxseeds).",
            "Spend 15 minutes daily in sunlight to enhance vitamin D levels."
        ],
        'source': 'Women’s Health Network'
    },
    ('Any', 'Any', 'Black', 'Any'): {
        'skin_condition': 'Hyperpigmentation & Dryness',
        'products': [
            ("Ambi Skincare Fade Cream", "https://www.amazon.com/dp/B000GD48T0"),
            ("SheaMoisture African Black Soap Balancing Moisturizer", "https://www.amazon.com/dp/B0038U4T32"),
        ],
        'lifestyle_changes': [
            "Apply sunscreen daily to protect against UV-induced hyperpigmentation.",
            "Increase consumption of vitamin C-rich foods (e.g., citrus fruits, berries).",
            "Maintain adequate hydration throughout the day."
        ],
        'source': 'Dermatology Times'
    },
    ('Any', 'Any', 'Asian', 'Any'): {
        'skin_condition': 'Pigmentation & Sensitive Skin',
        'products': [
            ("Hada Labo Tokyo Gentle Hydrating Cleanser", "https://www.amazon.com/dp/B00I4BUBN8"),
            ("Melano CC Intensive Anti-Spot Essence", "https://www.amazon.com/dp/B00ITAP8P0"),
        ],
        'lifestyle_changes': [
            "Limit sun exposure and use protective measures like hats and sunglasses.",
            "Include antioxidants in your diet (e.g., green tea, berries).",
            "Avoid harsh scrubs; opt for gentle exfoliants suitable for sensitive skin."
        ],
        'source': 'Dermatology Times'
    },
    ('Any', 'Any', 'Any', 'Happy'): {
        'skin_condition': 'Healthy & Glowing Skin',
        'products': [
            ("CeraVe AM Facial Moisturizing Lotion SPF 30", "https://www.amazon.com/dp/B00F97FHAW"),
            ("The Inkey List Omega Water Cream Moisturizer", "https://www.amazon.com/dp/B09BNZLQFC"),
        ],
        'lifestyle_changes': [
            "Maintain a balanced, vitamin-rich diet.",
            "Engage in regular physical activity.",
            "Drink plenty of water daily to keep skin hydrated."
        ],
        'source': 'General Advice'
    },
    ('Any', 'Any', 'Any', 'Neutral'): {
        'skin_condition': 'Balanced Skin',
        'products': [
            ("Cetaphil Daily Facial Cleanser", "https://www.amazon.com/dp/B00VK7RRAS"),
            ("Neutrogena Hydro Boost Hydrating Gel-Cream", "https://www.amazon.com/dp/B00NR1YQHM"),
        ],
        'lifestyle_changes': [
            "Establish and maintain a consistent skincare routine.",
            "Apply sunscreen daily to protect against UV damage.",
            "Avoid excessive alcohol consumption and refrain from smoking."
        ],
        'source': 'General Advice'
    },
}

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_container_width=True)

    with st.spinner('Analyzing your face...'):
        img_array = np.array(image)
        with face_analysis_lock:
            analysis = DeepFace.analyze(img_array, actions=['age', 'gender', 'emotion', 'race'], enforce_detection=False)

        age = analysis[0]['age']
        gender = analysis[0]['dominant_gender'].capitalize()
        race = analysis[0]['dominant_race'].capitalize()
        emotion_raw = analysis[0]['dominant_emotion'].lower()

        emotion_map = {
            'sad': 'Sad', 'angry': 'Stressed', 'fear': 'Anxious',
            'disgust': 'Anxious', 'happy': 'Happy', 'surprise': 'Happy',
            'neutral': 'Neutral', 'tired': 'Tired', 'fatigue': 'Tired'
        }

        emotion = emotion_map.get(emotion_raw, 'Neutral')
        age_group = '<25' if age < 25 else '25-40' if age <= 40 else '40+'

        keys = [
            (age_group, gender, race, emotion),
            (age_group, gender, 'Any', emotion),
            (age_group, 'Any', race, emotion),
            (age_group, 'Any', 'Any', emotion),
            ('Any', 'Any', race, 'Any'),
            ('Any', 'Any', 'Any', emotion),
            ('Any', 'Any', 'Any', 'Neutral')
        ]

        rec = next((recommendations[k] for k in keys if k in recommendations), recommendations[('Any', 'Any', 'Any', 'Neutral')])

    st.success(f"**Detected Condition:** {rec['skin_condition']}")
    st.info(f"Age: {age}, Gender: {gender}, Race: {race}, Mood: {emotion}")

    st.markdown("### 💡 Recommended Products")
    for prod, link in rec['products']:
        st.markdown(f"- [{prod}]({link})")

    st.markdown("### 🌿 Lifestyle Tips")
    for tip in rec['lifestyle_changes']:
        st.markdown(f"- {tip}")

    st.markdown(f"_Based on {rec['source']}_")
    st.markdown("🛒 *Affiliate links included.*")

st.markdown("---")
st.markdown("© 2024 Jaroslav Sidor. All rights reserved.")
