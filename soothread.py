import streamlit as st
import time

# --- ADD THIS FRAGMENT FUNCTION ---
@st.fragment
def study_timer():
    st.subheader("⏲️ Focus Timer")
    minutes = st.number_input("Set Timer (Minutes)", min_value=1, value=25, key="timer_input")
    
    if st.button("Start Focus Session"):
        timer_placeholder = st.empty()
        # By running inside a fragment, only THIS block refreshes
        # The main reading text will stay bright and clear!
        for i in range(minutes * 60, 0, -1):
            mins, secs = divmod(i, 60)
            timer_placeholder.metric("Time Remaining", f"{mins:02d}:{secs:02d}")
            time.sleep(1)
        st.success("Time's up! 🧘")
        st.balloons()

# --- UPDATE YOUR SIDEBAR CALL ---
with st.sidebar:
    st.title("🛠️ Study Tools")
    study_timer() # Call the fragment here
    
    st.divider()
    # ... rest of your sticky notes code ...
