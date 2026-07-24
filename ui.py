"""UI helpers for the GroqChat Streamlit app.

Keeps all rendering logic in one place so that app.py stays focused on
control flow and state management.
"""

import streamlit as st
from typing import List, Dict


def render_chat(messages: List[Dict[str, str]]) -> None:
    """Render the full conversation history.

    Args:
        messages: List of message dicts with "role" and "content" keys,
                  following the OpenAI-compatible format used by Groq.
                  Roles are "user" or "assistant".
    """
    for message in messages:
        role = message.get("role", "user")
        content = message.get("content", "")
        with st.chat_message(role):
            st.markdown(content)
