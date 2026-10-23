import os

import streamlit as st

os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

from research_agent import run_research  # noqa: E402

st.set_page_config(page_title="AI Research Agent", page_icon="🔎", layout="wide")
st.title("🔎 AI Research Agent")
st.caption("CrewAI + Groq (gpt-oss-120b) + DuckDuckGo")

# The API key is read only from Streamlit Secrets (set in the Streamlit Cloud dashboard).
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error(
        "GROQ_API_KEY not found. In Streamlit Cloud open your app, go to "
        "Settings > Secrets and add:\n\nGROQ_API_KEY = \"your_key_here\""
    )
    st.stop()

topic = st.text_input("Research topic", placeholder="e.g. Impact of AI on healthcare in 2026")

if st.button("Generate report", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Researching... this can take a minute."):
            try:
                st.session_state["report"] = run_research(topic.strip(), api_key)
            except Exception as e:
                st.error(f"Something went wrong: {e}")

if "report" in st.session_state:
    st.markdown(st.session_state["report"])
    st.download_button(
        "Download report (.md)",
        st.session_state["report"],
        file_name="research_report.md",
        mime="text/markdown",
    )
