import streamlit as st
from google import genai
from google.genai import types
import time

# --- 1. SETTINGS & CSS ---
st.set_page_config(page_title="Soothread", page_icon="📖", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; color: #e0e0e0; }
    .reading-text { font-family: 'serif'; font-size: 1.25rem; line-height: 1.8; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE TOOLS (Fragment fix for StreamlitAPIException) ---
@st.fragment
def sidebar_tools():
    # We use st.sidebar explicitly INSIDE the fragment to avoid the error in Image 7
    st.sidebar.title("🛠️ Study Tools")
    mins = st.sidebar.number_input("Focus Timer (Mins)", 1, 60, 25)
    
    if st.sidebar.button("Start Timer"):
        ph = st.sidebar.empty()
        for i in range(mins * 60, 0, -1):
            m, s = divmod(i, 60)
            ph.metric("Time Left", f"{m:02d}:{s:02d}")
            time.sleep(1)
        st.sidebar.success("Break time! 🧘")

# --- 3. SECURE CLIENT ---
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("Missing API Key in Streamlit Secrets!")
    st.stop()

# --- 4. MAIN APP LOGIC ---
sidebar_tools()

st.title("📖 Soothread Reader")
uploaded = st.file_uploader("Upload your study file", type=['txt'])

if uploaded:
    text = uploaded.read().decode("utf-8")
    st.markdown(f'<div class="reading-text">{text}</div>', unsafe_allow_html=True)
    
    if st.button("✨ Get Visual Learning Links"):
        with st.spinner("Finding diagrams and websites..."):
            try:
                # Proper 2026 configuration for Google Search tool
                search_tool = types.Tool(google_search=types.GoogleSearch())
                
                # WE USE FLASH-LITE HERE TO FIX THE 429 QUOTA ERROR (Image 3)
                response = client.models.generate_content(
                    model="gemini-2.0-flash-lite",
                    contents=f"Provide 3 educational website links with diagrams for: {text[:1000]}",
                    config=types.GenerateContentConfig(tools=[search_tool])
                )
                st.info(response.text)
            except Exception as e:
                st.error("The search service is busy. Please try again in 30 seconds.")
else:
    st.info("Please upload a .txt file to begin.")
