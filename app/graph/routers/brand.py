from app.graph.state import WebsiteBuilderState


def route_brand_approval(state: WebsiteBuilderState) -> str:
    status = state["brand_guideline_status"]
    if status == "approved":
        return "wireframe"
    if status == "revision_requested":
        return "brand_guideline"
    raise ValueError(f"Unexpected brand guideline status: {status}")
