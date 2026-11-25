from app.graph.state import WebsiteBuilderState


def route_location(state: WebsiteBuilderState) -> str:
    location = state.get("location")
    if (
        state.get("location_confirmed")
        and isinstance(location, str)
        and location.strip()
    ):
        return "manager_planning"

    return "location_clarification"