"""Generation endpoints for docs and code scaffold."""

from fastapi import APIRouter

from app.models.response_models import ArtifactListResponse
from app.orchestrator.workflow import WorkflowOrchestrator

router = APIRouter(prefix="/projects", tags=["generation"])
workflow = WorkflowOrchestrator()


@router.post("/{project_id}/docs", response_model=ArtifactListResponse)
def generate_docs(project_id: str) -> ArtifactListResponse:
    workflow.generate_docs(project_id)
    artifacts = workflow.project_service.list_artifacts(project_id)
    return ArtifactListResponse(project_id=project_id, artifacts=artifacts)


@router.post("/{project_id}/codegen", response_model=ArtifactListResponse)
def generate_code(project_id: str) -> ArtifactListResponse:
    workflow.generate_code(project_id)
    artifacts = workflow.project_service.list_artifacts(project_id)
    return ArtifactListResponse(project_id=project_id, artifacts=artifacts)
