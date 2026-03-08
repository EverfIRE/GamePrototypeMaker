"""Project endpoints."""

from fastapi import APIRouter

from app.models.request_models import CreateProjectRequest
from app.models.response_models import ArtifactListResponse, ProjectResponse
from app.orchestrator.workflow import WorkflowOrchestrator

router = APIRouter(prefix="/projects", tags=["projects"])
workflow = WorkflowOrchestrator()


@router.post("", response_model=ProjectResponse)
def create_project(request: CreateProjectRequest) -> ProjectResponse:
    state = workflow.project_service.create_project(
        title=request.title or "Untitled Prototype",
        raw_idea=request.raw_idea,
        target_platform=request.target_platform,
        target_engine=request.target_engine,
    )
    return ProjectResponse(project=state)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str) -> ProjectResponse:
    return ProjectResponse(project=workflow.project_service.get_project(project_id))


@router.get("/{project_id}/artifacts", response_model=ArtifactListResponse)
def list_artifacts(project_id: str) -> ArtifactListResponse:
    artifacts = workflow.project_service.list_artifacts(project_id)
    return ArtifactListResponse(project_id=project_id, artifacts=artifacts)
