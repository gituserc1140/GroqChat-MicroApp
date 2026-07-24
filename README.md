# GroqChat
AI chat micro-app powered by the Groq API

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://groqchat.streamlit.app/)
[![Sponsor me on GitHub](https://img.shields.io/badge/Sponsor%20me%20on-GitHub-EA4AAA?logo=githubsponsors&style=flat-square)](https://github.com/sponsors/gituserc1140)

## About

A lightweight Streamlit chat app that connects directly to the [Groq](https://console.groq.com/home) inference API — one of the fastest large-language-model backends available. Enter your Groq API key in the sidebar, choose a model, and start chatting instantly. Conversation history is preserved for the lifetime of your browser session, and a single click clears it when you want a fresh start.

## API key setup

You can provide your `GROQ_API_KEY` in any of these ways:

- Enter it in the Streamlit sidebar input field at runtime
- Add it to `.streamlit/secrets.toml`:
  ```
  GROQ_API_KEY = "gsk_..."
  ```
- Set it as an environment variable:
  ```
  GROQ_API_KEY=gsk_...
  ```

## Model selection

Use the sidebar model selector to switch between available Groq-hosted models:

- **llama3-8b-8192** — fast and efficient for everyday tasks (default)
- **llama3-70b-8192** — higher quality responses for complex reasoning
- **llama-3.1-8b-instant** — ultra-low latency
- **llama-3.3-70b-versatile** — best overall quality
- **mixtral-8x7b-32768** — long-context tasks (32 k token window)
- **gemma2-9b-it** — Google's Gemma 2 instruction-tuned model

## Quick start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Repository structure

| File / folder | Purpose |
|---|---|
| `app.py` | Streamlit entry-point — layout, session state, chat loop |
| `api_client.py` | Groq SDK wrapper; single `chat_completion()` function |
| `ui.py` | Rendering helpers (hero empty state, chat history) |
| `config/settings.py` | Model list, default model, env-var config |
| `requirements.txt` | Minimal Python dependencies |
