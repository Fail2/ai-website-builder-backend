import pytest

from app.agents.manager import manager_planning_node


@pytest.mark.asyncio
async def test_manager_creates_execution_plan():
    state = {
        "brand_name": "Test Hotel",
        "niche": "Hospitality",
        "location": "Dhaka, Bangladesh",
        "location_confirmed": True,
        "prompt": "Build a luxury hotel website.",
    }

    result = await manager_planning_node(state)

    assert "execution_plan" in result
    assert result["execution_plan"].goal
    assert len(result["execution_plan"].tasks) > 0
    assert result["current_stage"] == "planning"


@pytest.mark.asyncio
async def test_manager_rejects_unconfirmed_location():
    state = {
        "brand_name": "Test Hotel",
        "niche": "Hospitality",
        "location": None,
        "location_confirmed": False,
        "prompt": "Build a luxury hotel website.",
    }

    with pytest.raises(ValueError, match="Business location must be confirmed"):
        await manager_planning_node(state)