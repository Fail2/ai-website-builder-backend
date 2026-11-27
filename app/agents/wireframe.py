import json

from app.core.model import get_structurer_model
from app.schemas.wireframe import WireframeOutput


WIREFRAME_PROMPT = """
You are the Website Wireframe Agent for an autonomous website builder.

Create a practical, implementation-ready website blueprint from the supplied
business requirements, research reports, and approved brand guideline.

Your responsibilities:
- Recommend the pages this business actually needs.
- Define the primary navigation and menu labels.
- Define each page's purpose and its audience need.
- Define the ordered section hierarchy for every page.
- Describe each section's purpose, layout, content requirements, and UI
  components without writing the actual copy or code.
- Define a primary CTA and, where useful, a secondary CTA for each page.
- Incorporate relevant SEO topics and search intent.
- Identify global functionality needed by the website.

Rules:
- The approved brand guideline is authoritative. Do not change brand identity,
  colors, typography, or visual direction.
- Use niche, audience, competitor, and SEO research as evidence. Do not invent
  research findings, competitors, audience facts, or keyword metrics.
- Distinguish recommendations from sourced research where relevant.
- Recommend only pages justified by the business requirements, audience needs,
  and SEO research. Prefer a focused site over unnecessary pages.
- Include a homepage with page_slug "home".
- Use unique lowercase kebab-case page and section slugs.
- Navigation items must reference pages included in the output.
- Arrange sections in a logical visitor journey: orient, build trust, explain
  value, address objections, and convert where appropriate.
- Give each page a clear conversion goal and meaningful CTA.
- Describe layout structure, not visual styling. Visual styling belongs to the
  Design Agent.
- Do not write finished website copy, HTML, CSS, JavaScript, or image prompts.
- Do not create a sitemap, deployment plan, or QA checklist.
- If a previous wireframe and user feedback are supplied, revise only the
  affected pages or sections and preserve the rest of the structure.
- Return concise, specific, implementation-ready information that satisfies
  every field in the output schema.
"""


def execute_wireframe(
    brand_name: str,
    niche: str,
    location: str,
    user_requirements: str,
    research_context: dict,
    approved_brand_guideline: dict,
    previous_wireframe: dict | None = None,
    feedback: str | None = None,
) -> WireframeOutput:
    structured_model = get_structurer_model().with_structured_output(
        WireframeOutput,
        method="json_schema",
    )

    context = {
        "brand_name": brand_name,
        "niche": niche,
        "location": location,
        "user_requirements": user_requirements,
        "research_reports": research_context,
        "approved_brand_guideline": approved_brand_guideline,
        "previous_wireframe": previous_wireframe,
        "user_feedback": feedback,
    }

    return structured_model.invoke([
        ("system", WIREFRAME_PROMPT),
        ("human", json.dumps(context, ensure_ascii=False)),
    ])
