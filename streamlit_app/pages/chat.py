"""
Chat page for the Streamlit application.
"""

import streamlit as st
import os
import uuid

from utils.api_client import query_backend, document_upload_rag

# Configure page settings
st.set_page_config(
    page_title="Adaptive RAG · Chat",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": None,
        "Report a Bug": None,
        "About": None
    }
)

def load_css():
    """Load the premium UI CSS."""
    css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Hide Streamlit's default navigation & footer
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] { display: none; }
        [data-testid="stToolbar"]    { display: none; }
        footer                       { visibility: hidden; }
        header                       { background: transparent !important; }
    </style>
""", unsafe_allow_html=True)

# ---------- KNOWLEDGE BASE EXPANDER ----------
with st.expander("📂 KNOWLEDGE BASE & DOCUMENT UPLOAD", expanded=False):
    st.markdown("""
        <div style="font-size:0.8rem; color:#8B90B8; margin-bottom:15px;">
            Upload PDF or TXT documents here to add them to your AI's memory.
        </div>
    """, unsafe_allow_html=True)
    
    col_upload, col_active = st.columns([1, 1])
    
    with col_upload:
        uploaded_file = st.file_uploader(
            "Upload Document",
            type=["pdf", "txt"],
            label_visibility="collapsed"
        )

        if uploaded_file:
            file_description = st.text_input(
                "Describe this document",
                max_chars=300,
                placeholder="E.g. Q4 financial report",
                label_visibility="collapsed"
            )
            if "uploaded_files" not in st.session_state:
                st.session_state.uploaded_files = {}

            file_key = f"{uploaded_file.name}_{file_description}"

            if file_description:
                if file_key not in st.session_state.uploaded_files:
                    with st.spinner("Processing..."):
                        success = document_upload_rag(uploaded_file, file_description)
                    if success:
                        st.success(f"✓ Indexed: {uploaded_file.name}")
                        st.session_state.uploaded_files[file_key] = True
                    else:
                        st.error("Upload failed. Please try again.")
                else:
                    st.info(f"✓ Already indexed")
            elif uploaded_file:
                st.caption("↑ Describe your document to index it")

    with col_active:
        st.markdown("**Active Documents**")
        try:
            from utils.api_client import get_documents_rag, delete_document_rag
            
            docs = get_documents_rag()
            if docs:
                for d in docs:
                    st.markdown(f"""
                        <div style="
                            background:rgba(255,255,255,0.03);
                            border:1px solid rgba(255,255,255,0.07);
                            border-radius:8px; padding:8px 10px;
                            margin-bottom:6px; display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <div style="font-size:0.78rem; font-weight:500; color:#C4C9E8;">📄 {d['filename']}</div>
                                <div style="font-size:0.68rem; color:#4A4F6E; margin-top:2px;">{d['description'][:60]}...</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("🗑️ Remove", key=f"del_{d['id']}_{d['filename']}", help="Delete from memory"):
                        with st.spinner("Deleting..."):
                            delete_document_rag(d['filename'])
                            st.rerun()
            else:
                st.caption("No documents loaded.")
        except Exception as e:
            st.caption(f"Could not load documents: {str(e)}")

st.markdown("<hr style='margin-top:5px; margin-bottom:15px; border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)

if "show_logout_confirm" not in st.session_state:
    st.session_state.show_logout_confirm = False

# ---------- HEADER ----------
col_head1, col_head2, col_head3 = st.columns([8, 2, 2])
with col_head1:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:10px;">
            <div style="
                width:36px; height:36px; border-radius:10px;
                background: linear-gradient(135deg, #6C63FF, #FF6B9D);
                display:flex; align-items:center; justify-content:center;
                font-size:18px; box-shadow: 0 4px 15px rgba(108,99,255,0.4);">✦</div>
            <div>
                <div style="font-weight:700; font-size:1.4rem; color:#F0F2FF; letter-spacing:-0.02em;">Adaptive RAG</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
with col_head2:
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.chat_history = []
        import uuid
        session_id = uuid.uuid4().hex
        st.session_state["session_id"] = session_id
        st.session_state["jwt_token"] = session_id
        st.rerun()

with col_head3:
    if st.button("🔒 Sign Out", use_container_width=True):
        st.session_state.show_logout_confirm = True

if st.session_state.show_logout_confirm:
    st.warning("Sign out of this session?")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Yes", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.switch_page("home.py")
    with c2:
        if st.button("Cancel", use_container_width=True):
            st.session_state.show_logout_confirm = False

# ---------- SESSION INIT ----------
if "session_id" not in st.session_state:
    session_id = uuid.uuid4().hex
    st.session_state["session_id"] = session_id
    st.session_state["jwt_token"] = session_id
    st.session_state["username"] = "Guest"

if "chat_history" not in st.session_state:
    from utils.api_client import get_chat_history_rag
    st.session_state.chat_history = get_chat_history_rag(st.session_state.session_id)

# ---------- MAIN CHAT AREA ----------
# Empty state when no messages
if not st.session_state.chat_history:
    st.markdown("""
        <div style="display:flex; flex-direction:column; align-items:center;
             justify-content:center; padding:60px 20px; gap:16px; opacity:0.5;">
            <div style="font-size:3rem;">✦</div>
            <div style="font-size:1rem; font-weight:600; color:#8B90B8;">
                Ask me anything
            </div>
            <div style="font-size:0.82rem; color:#4A4F6E; text-align:center; max-width:350px; line-height:1.6;">
                I can chat, search the web, or answer questions<br>about your uploaded documents.
            </div>
        </div>
    """, unsafe_allow_html=True)

# Display chat history
for message in st.session_state.chat_history:
    if isinstance(message, dict):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    else:
        role, text = message
        with st.chat_message(role):
            st.markdown(text)

# ---------- INPUT ----------
# Handle new input
if prompt := st.chat_input("Message Adaptive RAG..."):
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant", avatar="✨"):
        status_placeholder = st.empty()
        
        def process_stream():
            for chunk in query_backend(prompt, st.session_state.session_id):
                if chunk.startswith("__NODE__") and chunk.endswith("|||"):
                    node_name = chunk.replace("__NODE__", "").replace("|||", "")
                    
                    if node_name == "retriever_node":
                        status_placeholder.info("📚 Reading your documents...")
                    elif node_name == "web_search":
                        status_placeholder.info("🌐 Searching the web...")
                    elif node_name == "generate":
                        status_placeholder.info("⚙️ Synthesizing final answer...")
                    elif node_name == "general_llm":
                        status_placeholder.info("🧠 Formulating response...")
                    else:
                        status_placeholder.info(f"🔄 Agent state: {node_name}...")
                else:
                    status_placeholder.empty()
                    yield chunk
                    
        full_response = st.write_stream(process_stream())
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})
