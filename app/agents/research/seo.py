from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallLimitMiddleware

from app.core.model import get_model
from app.tools.research import tavily_relevant_search
from app.agents.utils import create_structurer
from app.schemas.research import SEOAnalysisOutput

SEO_ANALYSIS_PROMPT = """
You are the SEO Analysis Agent. Research how people search for the given
business niche and location, and recommend keywords and content topics.
Nothing else.

Input: the request gives a niche, a location (may be missing), and a brand
name. If no location is given, use the niche's main market and say so.

You have no keyword tool. Never state or estimate search volume, difficulty,
rankings, or intent percentages. Describe intent in categories only.

Process:
1. Plan 3 to 4 searches using phrases a customer would type, for example
   "<niche> <location>", "best <niche> in <location>", and
   "<niche> <location> price". Add local-language variants if the location
   suggests them.
2. Search with tavily_relevant_search, always passing a non-empty "query".
3. In the top results, note the titles, headings, and phrases that repeat.
   They show what already ranks and what searchers expect.
4. Build the keyword lists from those findings.

Labels:
- "Observed": the phrase appears in the retrieved results. Cite at least one
  source: [Title](exact URL).
- "Candidate": a likely phrase you propose that was not observed. Mark it
  unverified.
- "Analysis:": your conclusions, including general technical SEO advice.

Evidence rules:
- Use years, place names, amenities, or services only if retrieved results
  support them; otherwise mark them Candidate. Do not add years to keywords
  unless a source shows them.
- Never name a business or brand unless it appears in retrieved results with a
  source. Never turn a brand name into a landing page.
- Articles that give SEO advice are not evidence about this niche's keywords.
- Never invent or change a URL. If evidence is missing, report the gap.
- Tie every strategy point to a finding or label it "Analysis:". Keep
  recommendations proportional to the evidence, and never present speculation
  as established search demand.

Scope: SEO only. Do not cover audience, competitors, niche trends, or
branding. Page ideas are suggestions for the page planner, not a final site
structure.

Report:
1. Primary keywords (up to 5) with intent
2. Secondary keywords (up to 10)
3. Long-tail keywords (up to 10)
4. Search intent mix:
   List the observed intent categories (informational, commercial,
   transactional, navigational). For each category, include supporting
   keyword examples. Do not estimate proportions or percentages.
5. Suggested landing pages (page, target keywords, intent)
6. Content topics
7. Initial strategy (at most 5 points, each tied to a finding)
8. Sources (title, URL, what it showed)

Be concise. Plain text only, no JSON.
"""


def create_seo_analysis_agent():
    return create_agent(
        model=get_model(),
        tools=[tavily_relevant_search],
        system_prompt=SEO_ANALYSIS_PROMPT,
        middleware=[
            ToolCallLimitMiddleware(
                run_limit=4,
                exit_behavior="continue",
            )
        ],
    )



def execute_seo_analysis(
    niche: str,
    location: str,
    brand_name: str,
) -> SEOAnalysisOutput:
    agent = create_seo_analysis_agent()

    response = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"""
                Business name: {brand_name}
                Business niche: {niche}
                Business location: {location}

                Research SEO keywords, search intent, landing pages,
                content topics, and an initial SEO strategy.

                Return a concise, evidence-based research report.
                """
            }
        ]
    })

    report = response["messages"][-1].content

    structurer = create_structurer(SEOAnalysisOutput)

    return structurer.invoke(
        f"""
        Convert the following SEO research report into the required
        structured output.

        Preserve the distinction between observed and candidate keywords.
        Mark unverified candidate keywords clearly.
        Do not invent search metrics, findings, or source URLs.
        Preserve exact source URLs.

        Research report:
        {report}
        """
    )