from pydantic import BaseModel, ConfigDict, Field, model_validator


class TaskPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    description: str
    assigned_agent: str
    dependencies: list[str] = Field(default_factory=list)
    status: str = "pending"


class ExecutionPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    goal: str
    tasks: list[TaskPlan] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_dependencies(self):
        task_ids = [task.task_id for task in self.tasks]

        if len(task_ids) != len(set(task_ids)):
            raise ValueError("Task IDs must be unique")

        for task in self.tasks:
            for dependency in task.dependencies:
                if dependency not in task_ids:
                    raise ValueError(
                        f"Unknown dependency '{dependency}' in task '{task.task_id}'"
                    )

                if dependency == task.task_id:
                    raise ValueError("A task cannot depend on itself")

        return self
