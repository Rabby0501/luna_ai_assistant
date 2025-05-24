import streamlit as st
import base64
import os
from modules.luna_core import (
    LUNA_SYSTEM_PROMPT,
    get_luna_response,
    text_to_speech,
    speech_to_text
)

# ---- Page Configuration ----
st.set_page_config(
    page_title="Luna AI Assistant",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---- Load Custom CSS ----
def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css()

# ---- Session State ----
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": LUNA_SYSTEM_PROMPT},
        {"role": "assistant", "content": "Hello lovely human! 🌸 How can I help?"}
    ]

# ---- Chat Interface ----
st.title("Luna AI Assistant 🌸✨")
# ---- Add File Verification ----
AVATAR_PATHS = {
    "user": "assets/user-avatar.png",
    "assistant": "assets/luna-avatar.png"
}

# Verify files exist
for role, path in AVATAR_PATHS.items():
    if not os.path.exists(path):
        st.error(f"Missing {role} avatar: {path}")
        st.stop()

# ---- Base64 Conversion with Error Handling ----
def get_image_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
        st.stop()

USER_AVATAR = f"data:image/png;base64,{get_image_base64(AVATAR_PATHS['user'])}"
LUNAS_AVATAR = f"data:image/png;base64,{get_image_base64(AVATAR_PATHS['assistant'])}"
# Display chat history


# ---- Input Section ----
input_col, voice_col = st.columns([5, 1])

with voice_col:
    if st.button("🎤", help="Start voice input"):
        try:
            user_input = speech_to_text()
            if user_input:
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.rerun()
        except Exception as e:
            st.error(f"Microphone access required: {str(e)}")

with input_col:
    user_input = st.chat_input("Type your message...")

if user_input:
    # Add and display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="assets/user-avatar.png"):
        st.markdown(user_input)
    
    # Generate and display response
    with st.chat_message("assistant", avatar="assets/luna-avatar.png"):
        response = st.write_stream(get_luna_response(st.session_state.messages))
        text_to_speech(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# ---- Sidebar ----
with st.sidebar:
    st.markdown("## Settings ⚙️")
    
    # Add temporary debug code to app.py
with st.sidebar:
    st.image("assets/user-avatar.png", width=100, caption="User Avatar Test")
    st.image("assets/luna-avatar.png", width=100, caption="Luna Avatar Test")
    
    if st.button("✨ Reset Conversation"):
        st.session_state.messages = [
            {"role": "system", "content": LUNA_SYSTEM_PROMPT},
            {"role": "assistant", "content": "Hello again! 🌸 Ready to chat?"}
        ]
        st.rerun()
    
    st.markdown("---")
    st.markdown("Built with 💖 using OpenAI & Streamlit")