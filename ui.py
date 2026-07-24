"""UI helpers for the GroqChat Streamlit app.

Keeps all rendering logic in one place so that app.py stays focused on
control flow and state management.
"""

import html
import streamlit as st
from typing import List, Dict

_ROLE_LABEL = {
    "user": "You",
    "assistant": "Groq",
}

_ROLE_ICON = {
    "user": "🧑",
    "assistant": "⚡",
}


def render_chat(messages: List[Dict[str, str]]) -> None:
    """Render the full conversation history.

    Args:
        messages: List of message dicts with "role" and "content" keys,
                  following the OpenAI-compatible format used by Groq.
                  Roles are "user" or "assistant".
    """
    if not messages:
        st.markdown(
            """
            <div style="
                text-align: center;
                padding: 3rem 1rem;
                color: #6b7280;
                font-size: 1rem;
            ">
                <p style="font-size:2rem; margin-bottom:0.5rem;">⚡</p>
                <p>Start a conversation — Groq responds at lightning speed.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    for message in messages:
        role = message.get("role", "user")
        content = message.get("content", "")
        icon = _ROLE_ICON.get(role, "🧑")
        with st.chat_message(role, avatar=icon):
            st.markdown(content)
