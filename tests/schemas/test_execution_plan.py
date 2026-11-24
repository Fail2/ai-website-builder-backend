import pytest
from pydantic import ValidationError

from app.schemas.execution_plan import TaskPlan


def test_valid_agent_is_accepted():
    task = TaskPlan(
        task_id="research_1",
        description="Analyze the niche",
        assigned_agent="niche_analysis_agent",
    )

    assert task.assigned_agent == "niche_analysis_agent"


def test_invalid_agent_is_rejected():
    with pytest.raises(ValidationError):
        TaskPlan(
            task_id="research_1",
            description="Analyze the niche",
            assigned_agent="unknown_agent",
        )

from app.schemas.execution_plan import ExecutionPlan


def test_duplicate_task_ids_are_rejected():
    with pytest.raises(ValidationError):
        ExecutionPlan(
            goal="Build a website",
            tasks=[
                TaskPlan(
                    task_id="task_1",
                    description="Research niche",
                    assigned_agent="niche_analysis_agent",
                ),
                TaskPlan(
                    task_id="task_1",
                    description="Research audience",
                    assigned_agent="audience_research_agent",
                ),
            ],
        )


def test_missing_dependency_is_rejected():
    with pytest.raises(ValidationError):
        ExecutionPlan(
            goal="Build a website",
            tasks=[
                TaskPlan(
                    task_id="task_1",
                    description="Research niche",
                    assigned_agent="niche_analysis_agent",
                    dependencies=["task_99"],
                ),
            ],
        )


def test_circular_dependencies_are_rejected():
    with pytest.raises(ValidationError):
        ExecutionPlan(
            goal="Build a website",
            tasks=[
                TaskPlan(
                    task_id="task_1",
                    description="Research niche",
                    assigned_agent="niche_analysis_agent",
                    dependencies=["task_2"],
                ),
                TaskPlan(
                    task_id="task_2",
                    description="Research audience",
                    assigned_agent="audience_research_agent",
                    dependencies=["task_1"],
                ),
            ],
        )

def test_invalid_task_status_is_rejected():
    with pytest.raises(ValidationError):
        TaskPlan(
            task_id="task_1",
            description="Research niche",
            assigned_agent="niche_analysis_agent",
            status="done",
        )