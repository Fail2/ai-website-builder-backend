from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class WireframeReviewRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: Literal["approve", "request_changes"]
    feedback: str | None = Field(default=None, max_length=2000)

    @model_validator(mode="after")
    def require_feedback_for_revision(self):
        if self.action == "request_changes" and not (self.feedback or "").strip():
            raise ValueError("Feedback is required when requesting changes.")
        return self
