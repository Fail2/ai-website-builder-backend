from langgraph.types import interrupt

from app.graph.state import WebsiteBuilderState


def location_clarification_node(
    state: WebsiteBuilderState,
) -> dict:
    # Location is already confirmed.
    if state.get("location_confirmed") and state.get("location"):
        return {
            "current_stage": "planning",
        }

    # Ask the user for the missing business location.
    user_location = interrupt({
        "type": "location_clarification",
        "question": "Which city and country is this business located in?",
    })

    if not isinstance(user_location, str) or not user_location.strip():
        raise ValueError("A valid business location is required.")

    return {
        "location": user_location.strip(),
        "location_confirmed": True,
        "current_stage": "planning",
    }