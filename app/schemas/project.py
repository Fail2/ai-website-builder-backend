from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import ProjectStatus


class ProjectCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    brand_name: str = Field(min_length=1, max_length=120)
    prompt: str = Field(min_length=10, max_length=5000)
    niche: str = Field(min_length=2, max_length=100)


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    brand_name: str
    prompt: str
    niche: str
    status: ProjectStatus
    created_at: datetime
