from functools import lru_cache

from app.core.config import settings
from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallLimitMiddleware

from app.core.model import create_model
from app.agents.utils import create_structurer
from app.schemas.research import ResearchOutput
from app.tools.research import (
    tavily_relevant_search,
    firecrawl_article_extract,
)

@lru_cache(maxsize=1)
def get_competitor_model():
    return create_model(settings.research_model_name, settings.competitor_model_api_key)

COMPETITOR_ANALYSIS_PROMPT = """
You are a Competitor Analysis Agent. Research competitors in the given
business niche and location. Produce a concise, evidence-based report.

Research process:
1. Use Tavily to identify 2–3 relevant competitors.
2. Prioritize direct competitors in the confirmed location.
3. Exclude the business being created.
4. Select competitors with verifiable official websites.
5. Use Firecrawl to inspect selected competitors' websites.
6. Base findings only on retrieved search results and inspected pages.

Analyze:
- Competitor names and exact official website URLs.
- Market positioning and key services.
- Notable website structure, features, and content approach.
- Evidence-based strengths and weaknesses.
- Opportunities for the new business to differentiate itself.

Evidence rules:
- Preserve exact URLs from Tavily or Firecrawl.
- Base website observations only on inspected pages.
- Distinguish conclusions using "Analysis:".
- Support strengths and weaknesses with specific evidence.
- Never invent competitors, URLs, or findings.
- Explicitly mention important evidence gaps.

Scope:
Focus exclusively on competitors and their websites.
Do not perform audience research, SEO analysis, or brand development.

Output:
- Plain text, not JSON.
- Maximum 1000 characters.
- Prioritize specific competitor names, URLs, findings, and
  differentiation opportunities.
- Avoid generic observations and unnecessary descriptions.
"""


def create_competitor_analysis_agent():
    return create_agent(
        model=get_competitor_model(),
        tools=[
            tavily_relevant_search,
            firecrawl_article_extract,
        ],
        system_prompt=COMPETITOR_ANALYSIS_PROMPT,
        middleware=[
            ToolCallLimitMiddleware(
                tool_name="tavily_relevant_search",
                run_limit=2,
                exit_behavior="continue",
            ),
            ToolCallLimitMiddleware(
                tool_name="firecrawl_article_extract",
                run_limit=3,
                exit_behavior="continue",
            ),
        ],
    )


def execute_competitor_analysis(
    niche: str,
    location: str,
    brand_name: str,
) -> ResearchOutput:
    agent = create_competitor_analysis_agent()

    response = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"""
                Business name: {brand_name}
                Business niche: {niche}
                Business location: {location}

                Research competitors for this business.
                Return a concise evidence-based research report.
                """
            }
        ]
    })

    research_report = response["messages"][-1].content
    
    structurer = create_structurer(ResearchOutput)

    return structurer.invoke(
        f"""
        Convert the research report into ResearchOutput.

        Rules:
        - Produce one descriptive competitor analysis report.
        - Maximum 1000 characters.
        - Preserve specific competitor names and exact URLs.
        - Summarize competitors' market positioning and key offerings.
        - Identify notable website features and content approaches.
        - Highlight competitor strengths and weaknesses where supported.
        - Include useful differentiation opportunities for the user's business.
        - Clearly distinguish sourced facts from analysis.
        - Do not invent or distort information.
        - Prioritize specific, useful findings over generic observations.

        Research report:
        {research_report}
        """
    )