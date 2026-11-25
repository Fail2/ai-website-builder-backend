from pydantic import BaseModel, ConfigDict, Field


class ResearchOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    report: str = Field(min_length=100, max_length=1000)