"""GroqChat – Streamlit front-end.

Users supply their own Groq API key (https://console.groq.com/keys) via the
sidebar, pick a model, and chat directly in the browser.  Conversation history
is kept in st.session_state for the lifetime of the browser session.

Run locally:
  pip install -r requirements.txt
  streamlit run app.py
"""

import streamlit as st
from config import settings
import api_client
import ui

st.set_page_config(page_title="GroqChat", page_icon="⚡", layout="centered")

_CSS = """
<style>
/* ── Page background ───────────────────────────────────────────── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0a0a, #1a1109, #0f0c07);
    min-height: 100vh;
}
[data-testid="stHeader"] { background: transparent; }

/* ── Hero banner ───────────────────────────────────────────────── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.hero h1 {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, #f97316, #fbbf24);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.hero p {
    color: #d1d5db;
    font-size: 1.05rem;
    margin-top: 0;
}

/* ── Chat message cards ────────────────────────────────────────── */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(249,115,22,0.2) !important;
    border-radius: 14px !important;
    margin-bottom: 0.6rem !important;
}

/* ── Buttons ───────────────────────────────────────────────────── */
[data-testid="stButton"] button {
    background: linear-gradient(135deg, #ea580c, #d97706) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.45rem 1.2rem !important;
    font-weight: 600 !important;
    transition: opacity 0.2s !important;
}
[data-testid="stButton"] button:hover { opacity: 0.85 !important; }

/* ── Chat input ────────────────────────────────────────────────── */
[data-testid="stChatInput"] textarea {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(249,115,22,0.35) !important;
    border-radius: 10px !important;
    color: #f3f4f6 !important;
}

/* ── Sidebar ───────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: rgba(10,10,10,0.9) !important;
    border-right: 1px solid rgba(249,115,22,0.2) !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div { color: #d1d5db !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2 {
    color: #f97316 !important;
}

/* ── Warning / error alerts ────────────────────────────────────── */
[data-testid="stAlert"] p { color: #ffffff !important; }

/* ── Spinner text ──────────────────────────────────────────────── */
[data-testid="stSpinner"] p { color: #fbbf24 !important; }

/* ── Selectbox & text inputs ───────────────────────────────────── */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.06) !important;
    border-color: rgba(249,115,22,0.35) !important;
}
</style>
"""

st.markdown(_CSS, unsafe_allow_html=True)

# ── Hero header ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <h1>⚡ GroqChat</h1>
        <p>Blazing-fast AI chat powered by <strong>Groq</strong> — the world's fastest inference engine.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Settings")

    api_key = st.text_input(
        "Groq API Key",
        value=settings.GROQ_API_KEY,
        type="password",
        placeholder="gsk_...",
        help="Get a free key at https://console.groq.com/keys",
    )

    default_model_index = (
        settings.AVAILABLE_MODELS.index(settings.DEFAULT_MODEL)
        if settings.DEFAULT_MODEL in settings.AVAILABLE_MODELS
        else 0
    )
    model = st.selectbox("Model", options=settings.AVAILABLE_MODELS, index=default_model_index)

    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<small><a href='https://console.groq.com/keys' target='_blank' "
        "style='color:#f97316;text-decoration:none;'>🔑 Get your free API key</a></small>",
        unsafe_allow_html=True,
    )

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Main chat area ────────────────────────────────────────────────────────────
ui.render_chat(st.session_state.messages)

user_input = st.chat_input("Ask anything…")

if user_input:
    if not api_key:
        st.warning("Please enter your Groq API key in the sidebar to start chatting.")
    else:
        # Snapshot the message count before appending so we can roll back cleanly on error
        snapshot_len = len(st.session_state.messages)

        # Append the user message and immediately show it
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        # Call the Groq API and display the response
        with st.chat_message("assistant"):
            with st.spinner("Thinking at the speed of Groq… ⚡"):
                try:
                    reply = api_client.chat_completion(
                        messages=st.session_state.messages,
                        model=model,
                        api_key=api_key,
                    )
                    st.markdown(reply)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": reply}
                    )
                except (ValueError, RuntimeError) as exc:
                    st.error(str(exc))
                    # Restore history to the pre-append snapshot so no partial
                    # messages are left behind regardless of what was added above
                    st.session_state.messages = st.session_state.messages[:snapshot_len]
