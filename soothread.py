import streamlit as st
from datetime import datetime
import time

# --- 1. PAGE SETUP & SOOTHING THEME ---
st.set_page_config(page_title="Serene Reader", page_icon="📖", layout="wide")

# Custom CSS for "Eye-Care" Typography and Colors
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@300&family=Inter:wght@400&display=swap');
    
    .stApp {
        background-color: #1a1a1a; /* Soft Dark Gray, not pure black */
        color: #e0e0e0;
    }
    .reading-text {
        font-family: 'Merriweather', serif; /* Best font for long reading */
        font-size: 1.2rem;
        line-height: 1.8;
        color: #d1d1d1;
        max-width: 800px;
        margin: auto;
        padding: 40px;
        background-color: #242424;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR UTILITIES (The "Hidden" Features) ---
with st.sidebar:
    st.title("🛠️ Study Tools")
    
    # Hidden Feature: Alarm/Timer
    st.subheader("⏲️ Focus Timer")
    minutes = st.number_input("Set Timer (Minutes)", min_value=1, value=25)
    if st.button("Start Focus Session"):
        with st.empty():
            for i in range(minutes * 60, 0, -1):
                mins, secs = divmod(i, 60)
                st.metric("Time Remaining", f"{mins:02d}:{secs:02d}")
                time.sleep(1)
            st.success("Time's up! Take a stretch break. 🧘")
            st.balloons()

    st.divider()
    
    # Hidden Feature: Sticky Notes
    st.subheader("📝 Quick Notes")
    if 'notes' not in st.session_state:
        st.session_state.notes = ""
    
    st.session_state.notes = st.text_area("Jot down important points:", 
                                          value=st.session_state.notes, 
                                          height=300)
    
    if st.button("Clear Notes"):
        st.session_state.notes = ""
        st.rerun()

# --- 3. MAIN INTERFACE ---
st.title("📖 Serene Reader")
st.caption("A distraction-free zone for deep learning.")

uploaded_file = st.file_uploader("Upload your study material (.txt only for now)", type=['txt'])

if uploaded_file is not None:
    # Reading the file
    content = uploaded_file.read().decode("utf-8")
    
    # Displaying the content in the "Reading Room"
    st.markdown(f'<div class="reading-text">{content}</div>', unsafe_allow_html=True)
else:
    st.info("👆 Please upload a text file to begin your reading session.")
    
    # Visual placeholder of how the simple layout works
    st.markdown("""
    ### Why this works for students:
    * **Serif Fonts:** We use 'Merriweather' which is scientifically easier on the eyes for long text.
    * **Low Contrast:** Instead of white on black, we use soft grays to prevent 'eye-burn'.
    * **Integrated Tools:** Your notes and timer stay in the sidebar, so you don't have to switch tabs.
    """)