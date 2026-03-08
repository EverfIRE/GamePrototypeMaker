"""Deterministic workflow orchestrator for project lifecycle."""

import json
from pathlib import Path

from app.agents.code_builder import CodeBuilder
from app.agents.design_doc_generator import DesignDocGenerator
from app.agents.idea_analyst import IdeaAnalyst
from app.agents.playtest_reviewer import PlaytestReviewer
from app.agents.prototype_planner import PrototypePlanner
from app.core.constants import WorkflowStage
from app.core.logger import get_logger
from app.models.domain_models import IdeaAnalysis, PlaytestReview, PrototypeScope
from app.orchestrator.state import VALID_TRANSITIONS
from app.services.codegen_service import CodegenService
from app.services.doc_service import DocService
from app.services.feedback_service import FeedbackService
from app.services.llm_service import LLMService
from app.services.project_service import ProjectService
from app.services.validation_service import ValidationService
from app.storage.fs_store import project_root


logger = get_logger(__name__)


class WorkflowOrchestrator:
    def __init__(self) -> None:
        self.project_service = ProjectService()
        llm_service = LLMService()
        self.idea_analyst = IdeaAnalyst(llm_service)
        self.prototype_planner = PrototypePlanner(llm_service)
        self.doc_generator = DesignDocGenerator(DocService())
        self.code_builder = CodeBuilder(CodegenService())
        self.playtest_reviewer = PlaytestReviewer(llm_service)
        self.feedback_service = FeedbackService()
        self.validation = ValidationService()

    def _transition(self, project_id: str, next_stage: str) -> None:
        current = self.project_service.get_project(project_id).current_stage
        self.validation.validate_transition(current, next_stage, VALID_TRANSITIONS)
        self.project_service.update_stage(project_id, next_stage)
        logger.info("Transition %s -> %s", current, next_stage)

    def _write_log(self, project_id: str, name: str, payload: str) -> None:
        log_path = project_root(project_id) / "logs" / name
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(payload, encoding="utf-8")

    def analyze_idea(self, project_id: str) -> IdeaAnalysis:
        project = self.project_service.get_project(project_id)
        output = self.idea_analyst.run(project.raw_idea)
        self.project_service.save_idea_analysis(project_id, output)
        self._write_log(project_id, "workflow.log", f"analyze_idea: {output.model_dump_json(indent=2)}")
        self._transition(project_id, WorkflowStage.IDEA_ANALYZED)
        return output

    def scope_prototype(self, project_id: str) -> PrototypeScope:
        idea_path = project_root(project_id) / "spec" / "idea_analysis.json"
        idea_data = json.loads(idea_path.read_text(encoding="utf-8"))
        idea = IdeaAnalysis(**idea_data)
        output = self.prototype_planner.run(idea)
        self.project_service.save_prototype_scope(project_id, output)
        self._transition(project_id, WorkflowStage.PROTOTYPE_SCOPED)
        return output

    def generate_docs(self, project_id: str) -> list[Path]:
        idea_data = json.loads((project_root(project_id) / "spec" / "idea_analysis.json").read_text(encoding="utf-8"))
        scope_data = json.loads((project_root(project_id) / "spec" / "prototype_scope.json").read_text(encoding="utf-8"))
        docs = self.doc_generator.run(IdeaAnalysis(**idea_data), PrototypeScope(**scope_data))

        written: list[Path] = []
        for name, content in docs.items():
            path = self.project_service.save_doc(project_id, name, content)
            written.append(path)
        self._transition(project_id, WorkflowStage.DOC_GENERATED)
        return written

    def generate_code(self, project_id: str) -> list[Path]:
        project = self.project_service.get_project(project_id)
        scope_data = json.loads((project_root(project_id) / "spec" / "prototype_scope.json").read_text(encoding="utf-8"))
        paths = self.code_builder.run(project_root(project_id) / "generated", project.target_engine, PrototypeScope(**scope_data))
        self.validation.require_files(paths)
        for p in paths:
            self.project_service.artifact_repo.add(project_id, str(p), "generated")
        self._transition(project_id, WorkflowStage.CODE_GENERATED)
        return paths

    def review_playtest(self, project_id: str, feedback_text: str) -> PlaytestReview:
        scope_data = json.loads((project_root(project_id) / "spec" / "prototype_scope.json").read_text(encoding="utf-8"))
        scope = PrototypeScope(**scope_data)
        review = self.playtest_reviewer.run(feedback_text, scope.prototype_goal)
        project = self.project_service.get_project(project_id)
        self.project_service.save_feedback_review(project_id, project.version, feedback_text, review)
        self.feedback_service.persist_review(project_id, project.version, feedback_text, review)
        self._transition(project_id, WorkflowStage.PLAYTEST_REVIEWED)
        return review

    def plan_next_iteration(self, project_id: str) -> dict[str, list[str]]:
        review_data = json.loads(
            (project_root(project_id) / "feedback" / f"review_v{self.project_service.get_project(project_id).version}.json").read_text(
                encoding="utf-8"
            )
        )
        review = PlaytestReview(**review_data)
        payload = {"next_experiments": review.next_experiments, "priority_changes": review.priority_changes}
        self.project_service.save_doc(project_id, "next_iteration_plan.json", json.dumps(payload, indent=2), kind="spec")
        self._transition(project_id, WorkflowStage.NEXT_ITERATION_PLANNED)
        return payload
