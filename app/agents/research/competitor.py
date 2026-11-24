from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallLimitMiddleware

from app.core.model import get_model
from app.agents.utils import create_structurer
from app.schemas.research import CompetitorAnalysisOutput
from app.tools.research import (
    tavily_relevant_search,
    firecrawl_article_extract,
)

COMPETITOR_ANALYSIS_PROMPT = """
You are a Competitor Analysis Agent. Your task is to identify and
evaluate competitors in the given business niche and location.

### Research Process

1. Use Tavily to find 2–3 relevant competitors.
2. Prioritize direct competitors operating in the confirmed location.
3. Exclude the business being created from the results.
4. Select competitors with verifiable official websites.
5. Use Firecrawl to inspect each selected competitor's website.
6. Analyze only information supported by search results or inspected pages.

### Analysis Criteria

For each competitor, examine:
- Market positioning and services.
- Website structure and page types.
- Features and functionality.
- Content strategy.
- Evidence-based strengths and weaknesses.

After analyzing competitors, identify opportunities for the new business
to differentiate itself.

### Evidence Requirements

- Use exact URLs returned by Tavily or Firecrawl.
- Base website findings only on pages actually inspected.
- Distinguish observed facts from your own conclusions using "Analysis:".
- Support strengths and weaknesses with specific evidence.
- Never invent competitors, URLs, features, or findings.
- If reliable evidence is unavailable, explicitly report the gap.

### Scope

Focus exclusively on competitor businesses and their websites.
Do not perform audience research, SEO analysis, or brand development.

### Report Format

1. Competitor profiles (analyze each competitor separately).
2. Differentiation opportunities.
3. Research sources (title, exact URL, and supported findings).

Keep the report concise and evidence-based.
"""


def create_competitor_analysis_agent():
    return create_agent(
        model=get_model(),
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
) -> CompetitorAnalysisOutput:
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

    report = response["messages"][-1].content

    structurer = create_structurer(CompetitorAnalysisOutput)

    return structurer.invoke(
        f"""
        Convert the following competitor research report into the
        required structured output.

        Do not invent missing information.
        Preserve exact competitor names and source URLs.

        Research report:
        {report}
        """
    )