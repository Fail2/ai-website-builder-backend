from langchain.agents import create_agent

from app.core.model import get_model
from app.schemas.research import CompetitorAnalysisOutput
from app.tools.research import (
    get_firecrawl_scrape_tool,
    get_tavily_search_tool,
)


COMPETITOR_ANALYSIS_PROMPT = """
You are a specialized Competitor Analysis Agent.

Your ONLY responsibility is to identify and analyze
business competitors and their websites.

You must:
1. Identify relevant competitors in the given business niche.
2. Analyze each competitor's market positioning.
3. Examine competitor website structures.
4. Identify common website features.
5. Analyze competitor content strategies.
6. Identify each competitor's strengths and weaknesses.
7. Find opportunities for business differentiation.
8. Provide reliable research sources.

Rules:
- Use Tavily to discover relevant competitors.
- Use Firecrawl to extract information from competitor websites.
- Analyze each competitor separately.
- Use evidence from actual websites where possible.
- Clearly distinguish observed facts from inferences.
- Do not research target audience demographics or personas.
- Do not perform keyword or SEO research.
- Do not generate brand guidelines.
- Do not invent competitors, findings, or sources.
- Return only the required structured output.
"""


def create_competitor_analysis_agent():
    return create_agent(
        model=get_model(),
        tools=[
            get_tavily_search_tool(),
            get_firecrawl_scrape_tool(),
        ],
        system_prompt=COMPETITOR_ANALYSIS_PROMPT,
        response_format=CompetitorAnalysisOutput,
    )
