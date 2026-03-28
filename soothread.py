import streamlit as st
from google import genai
import time

# --- 1. SETTINGS ---
st.set_page_config(page_title="Soothread", page_icon="📖", layout="wide")

# This CSS keeps the UI bright and high-contrast even when 'busy'
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; color: #e0e0e0; }
    .reading-area { font-family: 'serif'; font-size: 1.2rem; padding: 30px; line-height: 1.8; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURE API ---
try:
    # This pulls your key from the Streamlit "Secrets" tab
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.warning("⚠️ Please add your GEMINI_API_KEY to Streamlit Secrets!")
    st.stop()

# --- 3. THE TIMER (Fragment prevents fading) ---
@st.fragment
def sidebar_tools():
    with st.sidebar:
        st.title("🛠️ Tools")
        mins = st.number_input("Timer (Mins)", 1, 60, 25)
        if st.button("Start Timer"):
            ph = st.empty()
            for i in range(mins * 60, 0, -1):
                m, s = divmod(i, 60)
                ph.metric("Focus Time", f"{m:02d}:{s:02d}")
                time.sleep(1)
            st.success("Time up! 🧘")

sidebar_tools()

# --- 4. MAIN CONTENT ---
st.title("📖 Soothread Reader")
uploaded = st.file_uploader("Upload Study Material", type=['txt'])

if uploaded:
    text = uploaded.read().decode("utf-8")
    st.markdown(f'<div class="reading-area">{text}</div>', unsafe_allow_html=True)
else:
    st.info("Upload a file to begin reading.")

# --- 5. SMART SUMMARY (For your friend) ---
if st.button("✨ Summarize with Visual Links"):
    if uploaded:
        with st.spinner("Finding educational links..."):
            try:
                # USE FLASH-LITE TO AVOID THE 429 ERROR
                res = client.models.generate_content(
                    model="gemini-2.0-flash-lite", 
                    contents=f"Summarize this text and provide 2 educational web links for visual learners: {text[:2000]}"
                )
                st.info(res.text)
            except Exception as e:
                st.error("Server is busy. Please try again in 10 seconds.")
