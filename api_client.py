"""Groq API client module.

Wraps the official `groq` Python SDK to provide a single `chat_completion()`
function that the Streamlit app calls for every user message.
"""

from typing import List, Dict
from groq import Groq, AuthenticationError, APIConnectionError, RateLimitError


def chat_completion(
    messages: List[Dict[str, str]],
    model: str,
    api_key: str,
) -> str:
    """Send a list of chat messages to the Groq API and return the reply text.

    Args:
        messages: Conversation history in OpenAI-compatible format, e.g.
                  [{"role": "user", "content": "Hello"}]
        model:    Groq model identifier, e.g. "llama3-8b-8192".
        api_key:  Groq API key obtained from https://console.groq.com/keys.

    Returns:
        The assistant reply string.

    Raises:
        ValueError: If the API key is missing or clearly invalid.
        RuntimeError: On authentication, rate-limit, or connection errors.
    """
    if not api_key or not api_key.strip():
        raise ValueError(
            "A Groq API key is required. Get one at https://console.groq.com/keys"
        )

    client = Groq(api_key=api_key.strip())

    try:
        response = client.chat.completions.create(
            messages=messages,
            model=model,
        )
        if not response.choices:
            raise RuntimeError("Groq API returned an empty response (no choices).")
        content = response.choices[0].message.content
        if content is None:
            raise RuntimeError("Groq API returned a message with no content.")
        return content
    except AuthenticationError as exc:
        raise RuntimeError(
            "Invalid API key. Please check your key at https://console.groq.com/keys"
        ) from exc
    except RateLimitError as exc:
        raise RuntimeError(
            "Rate limit reached. Please wait a moment and try again."
        ) from exc
    except APIConnectionError as exc:
        raise RuntimeError(
            f"Could not connect to the Groq API: {exc}"
        ) from exc
