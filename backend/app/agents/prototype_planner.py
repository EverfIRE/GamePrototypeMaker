"""Prototype Planner agent."""

from app.models.domain_models import IdeaAnalysis, PrototypeScope
from app.services.llm_service import LLMService


class PrototypePlanner:
    def __init__(self, llm_service: LLMService) -> None:
        self.llm_service = llm_service

    def run(self, idea_analysis: IdeaAnalysis) -> PrototypeScope:
        return self.llm_service.scope_prototype(idea_analysis)
