"""Agent workflow endpoints for idea and scope stages."""

from fastapi import APIRouter

from app.models.response_models import IdeaAnalysisResponse, PrototypeScopeResponse
from app.orchestrator.workflow import WorkflowOrchestrator

router = APIRouter(prefix="/projects", tags=["agent"])
workflow = WorkflowOrchestrator()


@router.post("/{project_id}/analyze", response_model=IdeaAnalysisResponse)
def analyze_idea(project_id: str) -> IdeaAnalysisResponse:
    output = workflow.analyze_idea(project_id)
    return IdeaAnalysisResponse(project_id=project_id, analysis=output)


@router.post("/{project_id}/scope", response_model=PrototypeScopeResponse)
def scope_prototype(project_id: str) -> PrototypeScopeResponse:
    output = workflow.scope_prototype(project_id)
    return PrototypeScopeResponse(project_id=project_id, scope=output)
