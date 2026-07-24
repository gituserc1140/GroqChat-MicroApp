"""Configuration settings for the GroqChat micro-app.

API keys should be supplied by the end user via the Streamlit UI.
For production use you may also read them from environment variables or a
secret manager, but the UI input always takes precedence.

Get a free Groq API key at: https://console.groq.com/keys
"""

import os

# Groq API base URL (used by the groq SDK internally; exposed here for reference)
GROQ_API_BASE_URL = "https://api.groq.com"

# Optional: pre-fill the API key from an environment variable so that
# operators can set it without exposing it in the UI.
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Default chat model; users can override this from the UI.
DEFAULT_MODEL = os.getenv("GROQ_DEFAULT_MODEL", "llama3-8b-8192")

# Ordered list of models offered in the UI selector.
AVAILABLE_MODELS = [
    "llama3-8b-8192",
    "llama3-70b-8192",
    "llama-3.1-8b-instant",
    "llama-3.1-70b-versatile",
    "llama-3.3-70b-versatile",
    "mixtral-8x7b-32768",
    "gemma-7b-it",
    "gemma2-9b-it",
]

DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "30"))
