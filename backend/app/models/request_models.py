"""HTTP request contracts."""

from pydantic import BaseModel, Field


class CreateProjectRequest(BaseModel):
    title: str | None = None
    raw_idea: str = Field(min_length=5)
    target_platform: str = "PC"
    target_engine: str = "web"


class ReviewFeedbackRequest(BaseModel):
    feedback_text: str = Field(min_length=5)
