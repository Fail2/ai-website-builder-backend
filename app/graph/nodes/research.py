from app.graph.state import WebsiteBuilderState
from app.agents.research.niche import execute_niche_analysis
from app.agents.research.audience import execute_audience_research
from app.agents.research.competitor import execute_competitor_analysis
from app.agents.research.seo import execute_seo_analysis
from app.agents.brand import execute_brand_guideline


def niche_analysis_node(state: WebsiteBuilderState) -> dict:
    result = execute_niche_analysis(
        niche=state["niche"],
        location=state.get("location"),
    )
    print("niche result",result)
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
    print("audience result",result)
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
    print("competitor result",result)
    return {
        "agent_outputs": {
            "competitor_analysis": result.model_dump()
        }
    }


def seo_analysis_node(state: WebsiteBuilderState) -> dict:
    result = execute_seo_analysis(
        niche=state["niche"],
        location=state["location"],
        brand_name=state["brand_name"]
    )
    print("seo result",result)
    return {
        "agent_outputs": {
            "seo_analysis": result.model_dump()
        }
    }

def brand_guideline_node(state: WebsiteBuilderState) -> dict:
    agent_outputs = state["agent_outputs"]

    required_reports = [
        "niche_analysis",
        "audience_research",
        "competitor_analysis",
        "seo_analysis",
    ]

    if not all(
        key in agent_outputs and agent_outputs[key].get("report")
        for key in required_reports
    ):
        raise ValueError("Required research reports are missing.")

    research_context = {
        "niche_analysis": agent_outputs["niche_analysis"]["report"],
        "audience_research": agent_outputs["audience_research"]["report"],
        "competitor_analysis": agent_outputs["competitor_analysis"]["report"],
        "seo_analysis": agent_outputs["seo_analysis"]["report"],
    }

    result = execute_brand_guideline(
        brand_name=state["brand_name"],
        niche=state["niche"],
        location=state["location"],
        user_requirements=state["prompt"],
        research_context=research_context,
        previous_guideline=agent_outputs.get("brand_guideline"),
        feedback=state.get("brand_guideline_feedback"),
    )

    print("brand result",result)
    return {
        "agent_outputs": {
            "brand_guideline": result.model_dump()
        },
        "brand_guideline_status": "pending",
        "brand_guideline_feedback": "",
        "current_stage": "brand_guideline_review",
    }