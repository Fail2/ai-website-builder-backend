from langgraph.types import interrupt

from app.graph.state import WebsiteBuilderState


def brand_guideline_approval_node(state: WebsiteBuilderState) -> dict:
    decision = interrupt({
        "type": "brand_guideline_review",
        "brand_guideline": state["agent_outputs"]["brand_guideline"],
        "message": "Review the brand guideline and approve or request changes.",
    })
    action = decision.get("action")

    if action == "approve":
        return {
            "brand_guideline_status": "approved",
            "current_stage": "brand_guideline_approved",
        }

    if action == "request_changes":
        feedback = decision.get("feedback", "").strip()
        if not feedback:
            raise ValueError("Feedback is required when requesting changes.")
        return {
            "brand_guideline_status": "revision_requested",
            "brand_guideline_feedback": feedback,
            "current_stage": "brand_guideline_revision",
        }

    raise ValueError(f"Invalid approval action: {action}")
