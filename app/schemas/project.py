from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProjectStatus(str, Enum):
    CREATED = "created"
    PLANNING = "planning"
    RESEARCHING = "researching"
    AWAITING_BRAND_APPROVAL = "awaiting_brand_approval"
    PLANNING_PAGES = "planning_pages"
    GENERATING = "generating"
    QA = "qa"
    AWAITING_PUBLISH_APPROVAL = "awaiting_publish_approval"
    DEPLOYING = "deploying"
    COMPLETED = "completed"
    FAILED = "failed"


class ProjectCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    brand_name: str = Field(min_length=1, max_length=120)
    prompt: str = Field(min_length=10, max_length=5000)
    niche: str = Field(min_length=2, max_length=100)


class ProjectResponse(BaseModel):
    id: UUID
    brand_name: str
    prompt: str
    niche: str
    status: ProjectStatus
    created_at: datetime
