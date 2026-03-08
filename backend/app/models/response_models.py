"""HTTP response models."""

from pydantic import BaseModel

from app.models.domain_models import IdeaAnalysis, PlaytestReview, ProjectState, PrototypeScope


class ProjectResponse(BaseModel):
    project: ProjectState


class IdeaAnalysisResponse(BaseModel):
    project_id: str
    analysis: IdeaAnalysis


class PrototypeScopeResponse(BaseModel):
    project_id: str
    scope: PrototypeScope


class PlaytestReviewResponse(BaseModel):
    project_id: str
    review: PlaytestReview


class ArtifactListResponse(BaseModel):
    project_id: str
    artifacts: list[str]
