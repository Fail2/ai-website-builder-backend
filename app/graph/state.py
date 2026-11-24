from typing import Annotated, Any
from typing_extensions import TypedDict
import operator
from app.schemas.execution_plan import ExecutionPlan

class WebsiteBuilderState(TypedDict, total=False):
    # Initial user input
    project_id: str
    brand_name: str
    prompt: str
    niche: str
    location: str | None
    location_confirmed: bool

    # Manager's planning
    execution_plan: ExecutionPlan
    tasks: list[dict[str, Any]]

    # Worker agent results
    agent_outputs: Annotated[dict[str, Any], operator.or_]

    # Workflow tracking
    current_stage: str
    errors: Annotated[list[str], operator.add]