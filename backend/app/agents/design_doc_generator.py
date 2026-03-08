"""Design doc generator agent."""

from app.models.domain_models import IdeaAnalysis, PrototypeScope
from app.services.doc_service import DocService


class DesignDocGenerator:
    def __init__(self, doc_service: DocService) -> None:
        self.doc_service = doc_service

    def run(self, idea_analysis: IdeaAnalysis, prototype_scope: PrototypeScope) -> dict[str, str]:
        return {
            "prototype_brief.md": self.doc_service.build_prototype_brief(idea_analysis, prototype_scope),
            "test_plan.md": self.doc_service.build_test_plan(prototype_scope),
            "feature_list.json": self.doc_service.build_feature_list_json(prototype_scope),
        }
