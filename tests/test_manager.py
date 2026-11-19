import pytest

from app.core.model import get_model
from app.schemas.execution_plan import ExecutionPlan


@pytest.mark.asyncio
async def test_structured_execution_plan():
    model = get_model()
    structured_model = model.with_structured_output(ExecutionPlan)

    result = await structured_model.ainvoke(
        "Create a simple execution plan for a travel agency website. "
        "Include one niche analysis task."
    )

    assert isinstance(result, ExecutionPlan)
    assert result.goal
    assert len(result.tasks) >= 1