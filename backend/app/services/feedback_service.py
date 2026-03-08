"""Feedback-related domain service."""

from app.models.domain_models import PlaytestReview
from app.storage.repositories.feedback_repo import FeedbackRepository


class FeedbackService:
    def __init__(self) -> None:
        self.repo = FeedbackRepository()

    def persist_review(self, project_id: str, version: int, feedback_text: str, review: PlaytestReview) -> None:
        self.repo.add(project_id, version, feedback_text, review)
