from pydantic import BaseModel, ConfigDict, Field


class LocationExtraction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    location: str | None = Field(
        default=None,
        description="Explicit business location found in the prompt."
    )
    evidence: str | None = Field(
        default=None,
        description="Exact prompt substring that identifies the business location."
    )