from pydantic import BaseModel, ConfigDict, Field

class ResearchOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    report: str = Field(
        description=(
            "A concise research report containing no more than 150 words. "
            "Prioritize the most important evidence-based findings. "
            "Avoid repetition and unnecessary details."
        )
    )