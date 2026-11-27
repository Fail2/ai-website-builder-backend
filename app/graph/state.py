from typing import Annotated, Any, Literal
import operator

from typing_extensions import TypedDict

from app.schemas.execution_plan import ExecutionPlan


class WebsiteBuilderState(TypedDict, total=False):
    project_id: str
    brand_name: str
    prompt: str
    niche: str
    location: str | None
    location_confirmed: bool

    execution_plan: ExecutionPlan
    tasks: list[dict[str, Any]]
    agent_outputs: Annotated[dict[str, Any], operator.or_]

    brand_guideline_status: Literal["pending", "approved", "revision_requested"]
    brand_guideline_feedback: str

    wireframe_status: Literal["pending", "approved", "revision_requested"]
    wireframe_feedback: str

    current_stage: str
    errors: Annotated[list[str], operator.add]
