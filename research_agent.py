from datetime import date

from crewai import LLM, Agent, Crew, Process, Task

from search_tool import DuckDuckGoSearchTool

MODEL_NAME = "groq/openai/gpt-oss-120b"


def run_research(topic: str, api_key: str) -> str:
    # --- LLM ---
    llm = LLM(
        model=MODEL_NAME,
        api_key=api_key,
        temperature=0.3,
        max_tokens=4096,  # gpt-oss is a reasoning model, so give it extra room
    )

    # --- Agent ---
    researcher = Agent(
        role="Senior Research Analyst",
        goal="Research {topic} thoroughly and write an accurate, well-structured report.",
        backstory=(
            "You are an experienced analyst who searches the web, compares sources, "
            "and writes clear reports. You never invent facts or URLs."
        ),
        tools=[DuckDuckGoSearchTool()],
        llm=llm,
        allow_delegation=False,
        max_iter=6,
        verbose=False,
    )

    # --- Task ---
    task = Task(
        description=(
            "Research the topic: {topic}\n"
            "Today's date is {today}. Use the search tool several times with "
            "different queries, then write a report based only on what you found."
        ),
        expected_output=(
            "A markdown report with: a title, an executive summary, 3-5 key sections "
            "with headings, a short conclusion, and a 'Sources' list of URLs used."
        ),
        agent=researcher,
    )

    # --- Crew ---
    crew = Crew(
        agents=[researcher],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff(inputs={"topic": topic, "today": date.today().isoformat()})
    return result.raw
