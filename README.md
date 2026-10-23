# AI Research Agent

A single-agent research app built with CrewAI, Groq (`openai/gpt-oss-120b`), DuckDuckGo search and Streamlit.
Enter a topic and the agent searches the web and writes a markdown report.

## Deploy on Streamlit Community Cloud

1. Upload all these files to a GitHub repo (`app.py` must be in the repo root).
2. Go to https://share.streamlit.io and click **Create app**. Pick the repo, branch, and set main file to `app.py`.
3. Open **Advanced settings**, choose Python 3.12, and paste this into **Secrets**:

```toml
GROQ_API_KEY = "your_groq_key_here"
```

Get a free key at https://console.groq.com/keys. The app reads the key only from Streamlit Secrets, so never put it in the code.

## Troubleshooting

- **"GROQ_API_KEY not found":** add it under the app's Settings > Secrets, then reboot the app.
- **Groq rate limit:** wait a minute and retry (the free tier has per-minute limits).
- **Empty search results:** DuckDuckGo may rate-limit cloud IPs; the agent retries with new queries.
- **sqlite3 version error from chromadb:** add `pysqlite3-binary` to requirements.txt and put this at the very top of `app.py`:
  ```python
  __import__("pysqlite3")
  import sys; sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
  ```
- **Model not found:** check the current model ID at https://console.groq.com/docs/models and update `MODEL_NAME` in `research_agent.py`.
