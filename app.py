"""Main Streamlit application for AI Tutor"""

import streamlit as st
from config import CLASSES, SUBJECTS

st.set_page_config(
    page_title="AI Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎓 AI Tutor for Students")
st.markdown("Learn NCERT curriculum with AI-powered personalized tutoring")

# Sidebar: Subject and Class Selection
with st.sidebar:
    st.header("📚 Setup")
    
    selected_class = st.selectbox(
        "Select Class",
        CLASSES,
        format_func=lambda x: f"Class {x}"
    )
    
    selected_subject = st.selectbox(
        "Select Subject",
        list(SUBJECTS.keys())
    )
    
    st.markdown("---")
    st.header("📊 Progress")
    st.info("Radar chart showing strength per topic will appear here")
    
    st.markdown("---")
    st.header("👨‍🏫 Teacher View")
    if st.button("📄 Download Weekly Report"):
        st.success("Report generated! (Feature coming soon)")

# Main Chat Area
st.header(f"Learning: {selected_subject} - Class {selected_class}")

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input options
col1, col2 = st.columns([3, 1])

with col1:
    user_input = st.chat_input("Ask a question or say it aloud...")

with col2:
    voice_input = st.button("🎤 Voice Input", use_container_width=True)

# Process input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("assistant"):
        st.markdown("Thinking... (Feature coming soon)")
    st.session_state.messages.append({
        "role": "assistant",
        "content": "AI response will appear here"
    })
    st.rerun()

# Test Mode
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📝 Test Me (5 Questions)", use_container_width=True):
        st.info("Quiz mode coming soon")

with col2:
    if st.button("📖 Explain This Topic", use_container_width=True):
        st.info("Explanation feature coming soon")

with col3:
    if st.button("📊 View My Progress", use_container_width=True):
        st.info("Progress tracking coming soon")

# Footer
st.markdown("---")
st.markdown(
    "Built with ❤️ for educational equity | "
    "[Report Issue](https://github.com) | "
    "[NCERT PDFs](https://ncert.nic.in)"
)
