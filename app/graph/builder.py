from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from app.graph.routers.research import route_research_tasks

from app.graph.state import WebsiteBuilderState
from app.graph.nodes.location import location_clarification_node
from app.graph.nodes.research import (
    niche_analysis_node,
    audience_research_node,
    competitor_analysis_node,
    seo_analysis_node,
)
from app.agents.manager import manager_planning_node


builder = StateGraph(WebsiteBuilderState)

# Register nodes
builder.add_node("location_clarification", location_clarification_node)
builder.add_node("manager_planning", manager_planning_node)
builder.add_node("niche_analysis", niche_analysis_node)
builder.add_node("audience_research", audience_research_node)
builder.add_node("competitor_analysis", competitor_analysis_node)
builder.add_node("seo_analysis", seo_analysis_node)

# Initial flow
builder.add_edge(START, "location_clarification")
builder.add_edge("location_clarification", "manager_planning")

# Dynamically dispatch research tasks from the execution plan
builder.add_conditional_edges(
    "manager_planning",
    route_research_tasks,
)

# Each dispatched research node can finish independently
builder.add_edge("niche_analysis", END)
builder.add_edge("audience_research", END)
builder.add_edge("competitor_analysis", END)
builder.add_edge("seo_analysis", END)

# Temporary in-memory checkpointer for development
checkpointer = MemorySaver()

website_builder_graph = builder.compile(
    checkpointer=checkpointer
)