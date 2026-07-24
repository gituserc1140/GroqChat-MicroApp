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

st.set_page_config(page_title="GroqChat", page_icon="💬", layout="centered")

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Settings")

    api_key = st.text_input(
        "Groq API key",
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
        "Get a free API key at [console.groq.com/keys](https://console.groq.com/keys)"
    )

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Main chat area ────────────────────────────────────────────────────────────
st.title("💬 GroqChat")

ui.render_chat(st.session_state.messages)

user_input = st.chat_input("Type your message…")

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
            with st.spinner("Thinking…"):
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
