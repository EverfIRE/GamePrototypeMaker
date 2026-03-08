"""Idea Analyst agent."""

from app.models.domain_models import IdeaAnalysis
from app.services.llm_service import LLMService


class IdeaAnalyst:
    def __init__(self, llm_service: LLMService) -> None:
        self.llm_service = llm_service

    def run(self, raw_idea: str) -> IdeaAnalysis:
        return self.llm_service.analyze_idea(raw_idea)
