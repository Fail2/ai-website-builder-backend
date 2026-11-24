from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallLimitMiddleware

from app.core.model import get_model
from app.schemas.research import NicheAnalysisOutput
from app.tools.research import tavily_relevant_search

NICHE_ANALYSIS_PROMPT = """
You are the Niche Analysis Agent. Research the business niche in the user's
request and report evidence-based findings. Nothing else.

Input: the request gives a niche and may give a location. If no location is
given, research globally and say so.

Process:
1. You have very few searches, so make each query specific and broad enough to
   cover several topics (e.g. "<niche> market trends and challenges in <location>").
2. Search with tavily_relevant_search, always passing a non-empty "query".
3. Write the report using only what the search results say.

Evidence rules:
- End every factual claim with its source: [Title](exact URL from the results).
- Never invent facts, numbers, sources, or URLs. Never change a URL.
- If a topic has no supporting result, write "Not found in retrieved sources."
  Do not fill the gap from memory.
- Keep local findings and global findings separate. Never present global data
  as local.
- Label your own conclusions "Analysis:" so they are not mistaken for sourced facts.
- Industry terms may be defined from general knowledge; mark them "(general knowledge)".

Scope: the niche only. Do not cover audience, competitors, SEO, branding, or
website content.

Report sections:
1. Overview
2. Characteristics
3. Trends (local, global)
4. Opportunities
5. Challenges
6. Typical services and offerings
7. Terminology
8. Sources (title, URL, what it supported)

Be concise. Use bullets or tables. Plain text only, no JSON.
"""

def create_niche_analysis_agent():
    return create_agent(
        model=get_model(),
        tools=[tavily_relevant_search],
        system_prompt=NICHE_ANALYSIS_PROMPT,
        middleware=[
            ToolCallLimitMiddleware(
                tool_name="tavily_relevant_search",
                run_limit=2,
                exit_behavior="continue",
            )
        ],
    )


def create_niche_analysis_structurer():
    return get_model().with_structured_output(
        NicheAnalysisOutput,
        method="json_schema",
        strict=True,
    )


def execute_niche_analysis(
    niche: str,
    location: str | None = None,
) -> NicheAnalysisOutput:

    agent = create_niche_analysis_agent()

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Niche: {niche}\n"
                    f"Location: {location or 'not specified'}"
                ),
            }
        ]
    })

    research_report = result["messages"][-1].content

    structurer = create_niche_analysis_structurer()

    return structurer.invoke(
        f"""
        Convert this research report into NicheAnalysisOutput.

        Rules:
        - Use only information in the report.
        - Do not invent facts or sources.
        - Preserve exact source URLs.
        - Preserve missing information explicitly.

        Research report:
        {research_report}
        """
    )