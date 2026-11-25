from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Literal

class TaskPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str = Field(min_length=1)
    description: str
    assigned_agent: Literal[
        "niche_analysis_agent",
        "audience_research_agent",
        "competitor_analysis_agent",
        "seo_analysis_agent",
        "brand_agent",
        "wireframe_agent",
        "content_agent",
        "design_agent",
        "website_builder_agent",
    ]
    dependencies: list[str] = Field(default_factory=list)
    status: Literal[
        "pending",
        "in_progress",
        "completed",
        "failed",
    ] = "pending"


class ExecutionPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    goal: str
    tasks: list[TaskPlan] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_dependencies(self):
        task_ids = [task.task_id for task in self.tasks]

        if len(task_ids) != len(set(task_ids)):
            raise ValueError("Task IDs must be unique")

        dependency_map = {
            task.task_id: task.dependencies
            for task in self.tasks
        }

        for task in self.tasks:
            for dependency in task.dependencies:
                if dependency not in task_ids:
                    raise ValueError(
                        f"Unknown dependency '{dependency}' in task '{task.task_id}'"
                    )

                if dependency == task.task_id:
                    raise ValueError("A task cannot depend on itself")

        visited = set()
        visiting = set()

        def has_cycle(task_id: str) -> bool:
            if task_id in visiting:
                return True

            if task_id in visited:
                return False

            visiting.add(task_id)

            for dependency in dependency_map[task_id]:
                if has_cycle(dependency):
                    return True

            visiting.remove(task_id)
            visited.add(task_id)

            return False

        for task_id in task_ids:
            if has_cycle(task_id):
                raise ValueError("Circular task dependencies detected")

        return self
