from typing import Type

from crewai.tools import BaseTool
from ddgs import DDGS
from pydantic import BaseModel, Field


class SearchInput(BaseModel):
    query: str = Field(..., description="The web search query.")


class DuckDuckGoSearchTool(BaseTool):
    name: str = "DuckDuckGo Search"
    description: str = (
        "Searches the web with DuckDuckGo and returns titles, URLs and snippets. "
        "Use it to find current information on a topic."
    )
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        try:
            results = DDGS().text(query, max_results=5)
        except Exception as e:
            return f"Search failed: {e}. Try a different query."

        if not results:
            return "No results found. Try rewording the query."

        lines = []
        for i, r in enumerate(results, 1):
            title = r.get("title", "")
            url = r.get("href", "")
            body = (r.get("body") or "")[:300]  # keep it short to save tokens
            lines.append(f"{i}. {title}\n   URL: {url}\n   {body}")
        return "\n\n".join(lines)
