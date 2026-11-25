from app.core.model import get_model
from app.graph.state import WebsiteBuilderState
from app.schemas.execution_plan import ExecutionPlan

llm = get_model()

structured_llm = llm.with_structured_output(ExecutionPlan)

MANAGER_PROMPT = """
    You are the Manager Agent of an autonomous website builder.
    You plan the work; worker agents do it.

    Agents (use only these):
    - niche_analysis_agent: industry research
    - audience_research_agent: target audience and personas
    - competitor_analysis_agent: competitor research
    - seo_analysis_agent: keywords and search intent
    - brand_agent: brand guidelines
    - wireframe_agent: website pages, sections, and layouts
    - content_agent: website page content
    - design_agent: colors, fonts, and CSS styling
    - website_builder_agent: generates and edits static HTML, CSS, and JS files

    1. Understand the request
    - From the brand name, prompt, and niche, identify the website's purpose,
    business model, target market, and needed features.
    - Take the business location from the prompt. If it is missing or unclear,
    ask the user one clear question and stop. Never guess a location, and do
    not create a plan until it is confirmed.

    2. Create the plan
    - Use the fewest tasks that meet the request. Each task has a unique id,
    one agent, and its dependencies.
    - Research tasks (niche, audience, competitor, SEO) have no dependencies
    and run in parallel.
    - Brand guideline depends on research.
    Wireframe depends on brand approval.
    Content and design tasks depend on page confirmation.
    Website building depends on content and design tasks.
    - Never plan image generation, QA, sitemap, or deployment tasks.

    3. Coordinate
    - Check each output before passing it to a dependent task.
    - Retry a failed task within the limit, then reassign it or ask the user.
    - When requirements change, update the plan and rerun only the affected
    tasks. Keep finished results.
    - Stop for user approval after the brand guideline and after page confirmation.
    - Never invent an output or mark an unfinished task complete.
    """

async def manager_planning_node(
    state: WebsiteBuilderState,
) -> dict:
    
    if not state.get("location_confirmed") or not state.get("location"):
        raise ValueError(
            "Business location must be confirmed before planning."
        )

    user_prompt = f"""
    Brand name: {state["brand_name"]}

    Business niche: {state["niche"]}

    Location: {state["location"]}
    
    Website requirements:
    {state["prompt"]}
    """

    plan = await structured_llm.ainvoke(
        [
            ("system", MANAGER_PROMPT),
            ("human", user_prompt),
        ]
    )

    return {
        "execution_plan": plan,
        "current_stage": "planning",
    }