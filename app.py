import streamlit as st
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import google.generativeai as genai
import os
from dotenv import load_dotenv
import traceback

# -----------------------------
# ⚙️ Page Setup
# -----------------------------
st.set_page_config(
    page_title="PoetLens",
    page_icon="🌹",
    layout="centered",
)

# -----------------------------
# 💄 Custom Styling — Professional Wine Red Theme
# -----------------------------
st.markdown("""
<style>
/* Background gradient */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(145deg, #3b0a0a, #8b1a1a);
    color: #f8f4f4;
    font-family: 'Poppins', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #4a0e0e !important;
    color: #f5eaea !important;
}

/* Headings */
h1, h2, h3, h4 {
    color: #f8dcdc;
    font-weight: 600;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(90deg, #6b0f1a, #9b111e);
    color: white;
    font-weight: 600;
    border-radius: 10px;
    border: none;
    padding: 0.7rem 1.4rem;
    transition: 0.3s ease;
}
div.stButton > button:hover {
    background: linear-gradient(90deg, #8b1a1a, #a83232);
    transform: translateY(-2px);
}

/* Dropdowns */
div[data-baseweb="select"] > div {
    background-color: #fff5f5;
    color: #3b0a0a;
    border-radius: 8px;
    font-weight: 500;
}

/* File uploader */
[data-testid="stFileUploader"] {
    border: 2px dashed #f8dcdc;
    border-radius: 16px;
    padding: 1rem;
    background-color: rgba(255, 255, 255, 0.05);
}

/* Caption / Poem box */
.poem-box {
    background: rgba(255,255,255,0.08);
    border-left: 5px solid #f8dcdc;
    border-radius: 12px;
    padding: 1.2rem;
    margin-top: 1rem;
    color: #fff5f5;
    font-size: 1.1rem;
    line-height: 1.6;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

/* Selectbox label and subtext */
label, .stSelectbox label {
    color: #f8dcdc !important;
    font-weight: 500;
}

/* Download button */
.stDownloadButton > button {
    background: linear-gradient(90deg, #9b111e, #b32d2d);
    color: white;
    font-weight: 600;
    border-radius: 10px;
    padding: 0.6rem 1.2rem;
    border: none;
}
.stDownloadButton > button:hover {
    background: linear-gradient(90deg, #b32d2d, #d94f4f);
    transform: translateY(-2px);
}

/* Center content */
.block-container {
    max-width: 700px;
    padding-top: 2rem;
}

/* Subtle spinner text */
.stSpinner > div > div {
    color: #f8dcdc !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 🔑 Load API Key
# -----------------------------
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")



st.title("PoetLens")
st.markdown("<h4 style='color:#f8dcdc;'>Transform your photos into soulful poetry</h4>", unsafe_allow_html=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if not api_key:
    st.warning("Please set your GOOGLE_API_KEY in a .env file before running this app.")
else:
    genai.configure(api_key=api_key)

# -----------------------------
# Load BLIP Image Captioning
# -----------------------------
@st.cache_resource
def load_caption_model():
    caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    caption_model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    ).to(device)
    return caption_processor, caption_model

caption_processor, caption_model = load_caption_model()

# -----------------------------
# Upload Image
# -----------------------------
st.markdown("### Upload Your Image")
uploaded_file = st.file_uploader("Upload a photo (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

# -----------------------------
# Poem Settings
# -----------------------------
st.markdown("### Customize Your Poem")
col1, col2 = st.columns(2)

with col1:
    tone = st.selectbox(
        "Tone",
        ["nostalgic", "romantic", "haunting", "playful", "calm",
         "joyful", "melancholic", "mystical", "hopeful", "dark",
         "dreamy", "serene", "energetic", "tragic", "uplifting",
         "humorous", "spiritual", "philosophical", "patriotic", "adventurous"],
    )
    style = st.selectbox(
        "Style",
        ["free verse", "haiku", "sonnet", "rhyming couplets", "narrative poem", "acrostic"]
    )

with col2:
    length = st.selectbox("Length", ["short", "medium", "long"])
    language = st.selectbox("Language", ["English", "Tamil"])

# -----------------------------
# Poem Generation (Persistent)
# -----------------------------
if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Store poem in session_state
        if "generated_poem" not in st.session_state:
            st.session_state.generated_poem = None

        if st.button("Generate Poem"):
            with st.spinner("Generating your poem..."):
                # Step 1: Caption with BLIP
                inputs = caption_processor(images=image, return_tensors="pt")
                inputs = {k: v.to(device) for k, v in inputs.items()}
                out_ids = caption_model.generate(**inputs, max_new_tokens=40)
                caption = caption_processor.decode(out_ids[0], skip_special_tokens=True)

                # Step 2: Generate poem using Gemini
                model = genai.GenerativeModel("gemini-3.8-flash")

                if language == "English":
                    prompt = f"""
You are a creative poet. 
Write a {length} {style} poem in a {tone} tone in English, inspired by the following image description. 
Avoid repeating the caption directly. Use emotion and vivid imagery.

Image description: {caption}

Poem:
"""
                else:
                    prompt = f"""
நீங்கள் ஒரு படைப்பாற்றல்மிக்க கவிஞர். 
கீழே உள்ள பட விளக்கத்தின் அடிப்படையில் தமிழில் {tone} உணர்வில் {length} {style} கவிதை எழுதவும். 
கவிதை 4–8 வரிகளில் இருக்க வேண்டும். 
விளக்கத்தை நேரடியாக மீண்டும் எழுதாமல், கற்பனையும் உணர்வுகளையும் வெளிப்படுத்தும் பாணியில் எழுதவும்.

பட விளக்கம்: {caption}

கவிதை:
"""

                response = model.generate_content(prompt)
                poem = response.text.strip()

                # Save to session state
                st.session_state.generated_poem = poem

        # Display generated poem persistently
        if st.session_state.generated_poem:
            st.markdown("### Generated Poem")
            st.markdown(f"<div class='poem-box'>{st.session_state.generated_poem}</div>", unsafe_allow_html=True)
            st.download_button("Download Poem", st.session_state.generated_poem, file_name="poem.txt")

    except Exception:
        st.error("An unexpected error occurred.")
        st.text(traceback.format_exc())
