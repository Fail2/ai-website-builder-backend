from langgraph.types import interrupt

from app.agents.wireframe import execute_wireframe
from app.graph.state import WebsiteBuilderState


def wireframe_node(state: WebsiteBuilderState) -> dict:
    outputs = state.get("agent_outputs", {})
    required = (
        "niche_analysis",
        "audience_research",
        "competitor_analysis",
        "seo_analysis",
        "brand_guideline",
    )
    if any(key not in outputs for key in required):
        raise ValueError("Research reports and approved brand guideline are required.")

    if state.get("brand_guideline_status") != "approved":
        raise ValueError("Brand guideline must be approved before wireframe generation.")

    location = state.get("location")
    if not isinstance(location, str) or not location.strip():
        raise ValueError("A confirmed business location is required for wireframe generation.")

    research_context = {
        key: outputs[key]["report"]
        for key in required
        if key != "brand_guideline"
    }
    result = execute_wireframe(
        brand_name=state["brand_name"],
        niche=state["niche"],
        location=location.strip(),
        user_requirements=state["prompt"],
        research_context=research_context,
        approved_brand_guideline=outputs["brand_guideline"],
        previous_wireframe=outputs.get("wireframe"),
        feedback=state.get("wireframe_feedback"),
    )
    return {
        "agent_outputs": {"wireframe": result.model_dump()},
        "wireframe_status": "pending",
        "wireframe_feedback": "",
        "current_stage": "wireframe_review",
    }


def wireframe_approval_node(state: WebsiteBuilderState) -> dict:
    decision = interrupt({
        "type": "wireframe_review",
        "wireframe": state["agent_outputs"]["wireframe"],
        "message": "Review the recommended pages and wireframes. Approve or request changes.",
    })
    action = decision.get("action")

    if action == "approve":
        return {
            "wireframe_status": "approved",
            "current_stage": "wireframe_approved",
        }

    if action == "request_changes":
        feedback = decision.get("feedback", "").strip()
        if not feedback:
            raise ValueError("Feedback is required when requesting wireframe changes.")
        return {
            "wireframe_status": "revision_requested",
            "wireframe_feedback": feedback,
            "current_stage": "wireframe_revision",
        }

    raise ValueError(f"Invalid wireframe review action: {action}")
