from langgraph.graph import END, START, StateGraph

from app.agents.manager import manager_planning_node
from app.graph.nodes.approval import brand_guideline_approval_node
from app.graph.nodes.location import (
    location_clarification_node,
    location_extraction_node,
)
from app.graph.nodes.research import (
    audience_research_node,
    brand_guideline_node,
    competitor_analysis_node,
    niche_analysis_node,
    seo_analysis_node,
)
from app.graph.nodes.validation import research_validation_node
from app.graph.nodes.wireframe import wireframe_approval_node, wireframe_node
from app.graph.routers.brand import route_brand_approval
from app.graph.routers.location import route_location
from app.graph.routers.research import route_research_tasks
from app.graph.routers.wireframe import route_wireframe_review
from app.graph.state import WebsiteBuilderState


builder = StateGraph(WebsiteBuilderState)

builder.add_node("location_extraction", location_extraction_node)
builder.add_node("location_clarification", location_clarification_node)
builder.add_node("manager_planning", manager_planning_node)
builder.add_node("niche_analysis", niche_analysis_node)
builder.add_node("audience_research", audience_research_node)
builder.add_node("competitor_analysis", competitor_analysis_node)
builder.add_node("seo_analysis", seo_analysis_node)
builder.add_node("research_validation", research_validation_node)
builder.add_node("brand_guideline", brand_guideline_node)
builder.add_node("brand_guideline_approval", brand_guideline_approval_node)
builder.add_node("wireframe", wireframe_node)
builder.add_node("wireframe_approval", wireframe_approval_node)

builder.add_edge(START, "location_extraction")
builder.add_conditional_edges(
    "location_extraction",
    route_location,
    {
        "manager_planning": "manager_planning",
        "location_clarification": "location_clarification",
    },
)
builder.add_edge("location_clarification", "manager_planning")
builder.add_conditional_edges("manager_planning", route_research_tasks)
builder.add_edge(
    ["niche_analysis", "audience_research", "competitor_analysis", "seo_analysis"],
    "research_validation",
)
builder.add_edge("research_validation", "brand_guideline")
builder.add_edge("brand_guideline", "brand_guideline_approval")
builder.add_conditional_edges(
    "brand_guideline_approval",
    route_brand_approval,
    {
        "brand_guideline": "brand_guideline",
        "wireframe": "wireframe",
    },
)
builder.add_edge("wireframe", "wireframe_approval")
builder.add_conditional_edges(
    "wireframe_approval",
    route_wireframe_review,
    {
        "wireframe": "wireframe",
        "end": END,
    },
)


def compile_website_builder_graph(checkpointer):
    return builder.compile(checkpointer=checkpointer)
