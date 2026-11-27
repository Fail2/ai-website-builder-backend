from app.graph.state import WebsiteBuilderState


def route_wireframe_review(state: WebsiteBuilderState) -> str:
    status = state["wireframe_status"]
    if status == "approved":
        return "end"
    if status == "revision_requested":
        return "wireframe"
    raise ValueError(f"Unexpected wireframe status: {status}")
