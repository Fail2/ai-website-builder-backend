from functools import lru_cache
from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallLimitMiddleware

from app.core.model import create_model
from app.core.config import settings
from app.schemas.research import ResearchOutput
from app.tools.research import tavily_relevant_search
from app.agents.utils import create_structurer

@lru_cache(maxsize=1)
def get_audience_model():
    return create_model(settings.research_model_name, settings.audience_model_api_key)

AUDIENCE_RESEARCH_PROMPT = """
You are the Audience Research Agent. Research who the customers of the given
business niche are and report evidence-based findings. Nothing else.
 
Input: the request gives a niche and may give a location and a brand name.
If no location is given, research globally and say so.
 
Process:
1. You have few searches, so plan 3 to 4 specific queries. Cover who buys,
   what problems and goals customers mention, and how they search and decide.
   Use review, forum, and survey wording, e.g.
   "<niche> customer complaints and reviews <location>".
2. Search with tavily_relevant_search, always passing a non-empty "query".
3. Write the report using only what the search results say.
 
Evidence rules:
- End every factual claim with its source: [Title](exact URL from the results).
- Never invent demographics, percentages, quotes, sources, or URLs.
  Never change a URL.
- If a topic has no supporting result, write "Not found in retrieved sources."
- Keep local findings and global findings separate.
- Label your own conclusions "Analysis:".
- A persona is a summary built from the segments and needs you found. Mark each
  persona "Evidence: sourced", "partly inferred", or "inferred", and list the
  findings it rests on.

Persona rules:
- Never invent names or present fictional individuals as researched customers.
- Build personas from evidence-supported audience segments.
- Use anonymous labels such as "Corporate Business Traveler".
- Include only supported characteristics.
- Mark every characteristic as either "Evidence" or "Analysis".
- If there is insufficient evidence to build a persona, explicitly
  state "Insufficient evidence to create a reliable persona."
 
Scope: the audience only. Do not cover niche trends, competitors, SEO,
branding, or website content.

Report length:
- Keep the complete report within 1000 characters.
- Prioritize evidence-backed findings when space is limited.
 
Report sections:
1. Primary segments (who buys, who decides)
2. Secondary segments
3. Needs, goals, and pain points
4. Buying behavior (how they search, compare, decide, and pay or book)
5. Personas (2 to 3)
6. Research gaps
7. Sources (title, URL, what it supported)
 
Be concise. Use bullets or tables. Plain text only, no JSON.
"""


def create_audience_research_agent():
    return create_agent(
        model=get_audience_model(),
        tools=[tavily_relevant_search],
        system_prompt=AUDIENCE_RESEARCH_PROMPT,
        middleware=[
            ToolCallLimitMiddleware(
                tool_name="tavily_relevant_search",
                run_limit=4,
                exit_behavior="continue",
            )
        ],
    )


def execute_audience_research(
    niche: str,
    location: str,
) -> ResearchOutput:

    agent = create_audience_research_agent()

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Niche: {niche}\n"
                    f"Location: {location}"
                ),
            }
        ]
    })

    research_report = result["messages"][-1].content
    
    structurer = create_structurer(ResearchOutput)

    return structurer.invoke(
        f"""
        Convert the audience research report into ResearchOutput.

        Rules:
        - Produce one descriptive audience research report.
        - Maximum 1000 characters.
        - Preserve the most important audience segments,
        needs, pain points, and buying behavior.
        - Include evidence-based personas when available.
        - Preserve important supporting findings and exact URLs.
        - Clearly distinguish sourced facts from analysis and inference.
        - Do not invent or distort information.
        - Prioritize useful audience insights over generic observations.

        Research report:
        {research_report}
        """
    )