import json

from app.core.model import get_brand_model
from app.schemas.brand_guideline import BrandGuideline


BRAND_GUIDELINE_PROMPT = """
You are the Brand Guideline Agent. Turn the research reports and brand
requirements below into a brand guideline, filling every field of the schema.
Follow each field's description carefully.

Inputs: brand name, niche, location, user requirements, and four research
reports (niche, audience, competitor, SEO). If a previous guideline and user
feedback are provided, change only what the feedback affects and keep every
other field exactly as it was.

Rules:
- Base positioning, messaging, and tone on the research. Never invent research
  findings, business facts, competitors, or reference websites or URLs.
- Do not present inferred, candidate, or unverified findings as facts.
- If research is missing or conflicting, make cautious recommendations based
  only on available information.
- Fit the business's location and culture.
- Colors: exact HEX codes, each with its use. Choose text and background pairs
  with strong contrast.
- Fonts: use only free Google Fonts.
- Logo direction: provide text-based implementation guidance. Specify the logo
  type, brand-name typography, and a simple icon concept implementable with
  inline SVG or CSS. Use the defined palette and fonts. Do not generate an
  actual logo.
- Visual identity: describe CSS-friendly design properties such as corner
  radius, shadows, spacing, background patterns or gradients, icon style,
  and overall mood. Do not repeat image photography guidance here.
- Image guidelines: describe image requirements for relevant website sections,
  including subjects, photography or illustration style, composition, lighting,
  and mood. Specify palette-based placeholders for unavailable images.
  Do not generate actual images.
- UI/UX direction: provide actionable layout, hierarchy, spacing, and
  interaction guidance consistent with the brand.
- Brand messaging must include one tagline and three distinct value
  propositions.
- Design inspiration: identify relevant design styles. Do not invent websites
  or URLs.
- Be concise and actionable. Do not repeat points across fields. Respect each
  field's length limit, and keep the whole guideline under 4,000 characters.
"""



def execute_brand_guideline(
    brand_name: str,
    niche: str,
    location: str,
    user_requirements: str,
    research_context: dict,
    previous_guideline: dict | None = None,
    feedback: str | None = None,
) -> BrandGuideline:
    structured_model = get_brand_model().with_structured_output(
        BrandGuideline,
        method="json_schema",
        strict=True,
    )

    context = {
        "brand_name": brand_name,
        "niche": niche,
        "location": location,
        "user_requirements": user_requirements,
        "research_reports": research_context,
        "previous_guideline": previous_guideline,
        "user_feedback": feedback,
    }

    return structured_model.invoke([
        ("system", BRAND_GUIDELINE_PROMPT),
        ("human", json.dumps(context, ensure_ascii=False)),
    ])