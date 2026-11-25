from app.graph.state import WebsiteBuilderState
from app.agents.research.niche import execute_niche_analysis
from app.agents.research.audience import execute_audience_research
from app.agents.research.competitor import execute_competitor_analysis
from app.agents.research.seo import execute_seo_analysis


def niche_analysis_node(state: WebsiteBuilderState) -> dict:
    result = execute_niche_analysis(
        niche=state["niche"],
        location=state.get("location"),
    )
    return {
        "agent_outputs": {
            "niche_analysis": result.model_dump()
        }
    }


def audience_research_node(state: WebsiteBuilderState) -> dict:
    result = execute_audience_research(
        niche=state["niche"],
        location=state["location"],
    )
    return {
        "agent_outputs": {
            "audience_research": result.model_dump()
        }
    }


def competitor_analysis_node(state: WebsiteBuilderState) -> dict:
    result = execute_competitor_analysis(
        niche=state["niche"],
        location=state["location"],
        brand_name=state["brand_name"],
    )
    return {
        "agent_outputs": {
            "competitor_analysis": result.model_dump()
        }
    }


def seo_analysis_node(state: WebsiteBuilderState) -> dict:
    result = execute_seo_analysis(
        niche=state["niche"],
        location=state["location"],
    )
    return {
        "agent_outputs": {
            "seo_analysis": result.model_dump()
        }
    }