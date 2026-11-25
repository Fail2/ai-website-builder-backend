from langgraph.types import Send

from app.graph.state import WebsiteBuilderState


RESEARCH_AGENT_NODES = {
    "niche_analysis_agent": "niche_analysis",
    "audience_research_agent": "audience_research",
    "competitor_analysis_agent": "competitor_analysis",
    "seo_analysis_agent": "seo_analysis",
}


def route_research_tasks(state: WebsiteBuilderState) -> list[Send]:
    plan = state["execution_plan"]

    sends = []

    for task in plan.tasks:
        node_name = RESEARCH_AGENT_NODES.get(task.assigned_agent)

        if node_name is None:
            continue

        if task.status != "pending":
            continue

        if task.dependencies:
            continue

        sends.append(
            Send(
                node_name,
                state,
            )
        )

    if not sends:
        raise ValueError("No executable research tasks found in execution plan.")

    return sends