"""Feedback endpoints for review and next iteration."""

from fastapi import APIRouter

from app.models.request_models import ReviewFeedbackRequest
from app.models.response_models import PlaytestReviewResponse
from app.orchestrator.workflow import WorkflowOrchestrator

router = APIRouter(prefix="/projects", tags=["feedback"])
workflow = WorkflowOrchestrator()


@router.post("/{project_id}/review", response_model=PlaytestReviewResponse)
def review_feedback(project_id: str, request: ReviewFeedbackRequest) -> PlaytestReviewResponse:
    review = workflow.review_playtest(project_id, request.feedback_text)
    return PlaytestReviewResponse(project_id=project_id, review=review)


@router.post("/{project_id}/iterate")
def plan_next_iteration(project_id: str) -> dict[str, list[str]]:
    return workflow.plan_next_iteration(project_id)
