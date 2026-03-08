"""Playtest reviewer agent."""

from app.models.domain_models import PlaytestReview
from app.services.llm_service import LLMService


class PlaytestReviewer:
    def __init__(self, llm_service: LLMService) -> None:
        self.llm_service = llm_service

    def run(self, feedback_text: str, current_goal: str) -> PlaytestReview:
        return self.llm_service.review_playtest(feedback_text, current_goal)
