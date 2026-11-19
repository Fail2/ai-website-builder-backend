from app.core.model import get_model
from app.graph.state import WebsiteBuilderState
from app.schemas.execution_plan import ExecutionPlan

llm = get_model()

structured_llm = llm.with_structured_output(ExecutionPlan)


async def manager_planning_node(
    state: WebsiteBuilderState,
) -> dict:
    system_prompt = """
    You are the Manager Agent of an autonomous AI website builder.

    Analyze the user's requirements and create a structured execution plan.

    Available agents:
    - niche_analysis_agent
    - audience_research_agent
    - competitor_analysis_agent
    - seo_analysis_agent
    - brand_agent
    - page_planning_agent
    - content_agent
    - design_agent
    - image_agent
    - website_builder_agent
    - editing_agent
    - deployment_agent

    Planning rules:
    1. Break the website-building process into clear, manageable tasks.
    2. Assign each task to the most appropriate agent.
    3. Define dependencies between tasks.
    4. Independent research tasks should have no dependencies,
       allowing them to run in parallel.
    5. Brand guideline creation must depend on the required
       research tasks.
    6. Page planning must depend on brand guideline approval.
    7. Website generation must depend on the required content,
       design, and image tasks.
    8. Do not include wireframe or sitemap generation tasks.
    9. Use unique task IDs.
    10. Keep the plan relevant to the user's requirements.
    """

    user_prompt = f"""
    Brand name: {state["brand_name"]}

    Business niche: {state["niche"]}

    Website requirements:
    {state["prompt"]}
    """

    plan = await structured_llm.ainvoke(
        [
            ("system", system_prompt),
            ("human", user_prompt),
        ]
    )

    return {
        "execution_plan": plan,
        "current_stage": "planning",
    }