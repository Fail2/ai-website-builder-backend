from app.graph.state import WebsiteBuilderState


REQUIRED_RESEARCH_OUTPUTS = {
    "niche_analysis",
    "audience_research",
    "competitor_analysis",
    "seo_analysis",
}


def research_validation_node(state: WebsiteBuilderState) -> dict:
    agent_outputs = state.get("agent_outputs", {})

    missing_outputs = REQUIRED_RESEARCH_OUTPUTS - set(agent_outputs.keys())

    if missing_outputs:
        raise ValueError(
            f"Missing research outputs: {sorted(missing_outputs)}"
        )

    invalid_outputs = [
        name
        for name in REQUIRED_RESEARCH_OUTPUTS
        if not isinstance(agent_outputs[name], dict) or not agent_outputs[name]
    ]

    if invalid_outputs:
        raise ValueError(
            f"Invalid or empty research outputs: {sorted(invalid_outputs)}"
        )

    return {
        "current_stage": "research_completed",
    }