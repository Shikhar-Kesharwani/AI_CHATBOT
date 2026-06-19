"""
Home page for Streamlit interface (Bypassing missing auth backend).
"""

import logging
import streamlit as st
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log",
    filemode="a",
)

# Bypass login and just generate a local session identifier
if "session_id" not in st.session_state:
    session_id = uuid.uuid4().hex
    st.session_state["session_id"] = session_id
    st.session_state["jwt_token"] = session_id  # The backend just uses this to track history
    st.session_state["username"] = "Guest"

# Automatically jump to chat
st.switch_page("pages/chat.py")
