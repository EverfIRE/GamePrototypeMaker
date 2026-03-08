"""Project-level persistence and file operations."""

from pathlib import Path

from app.core.constants import WorkflowStage
from app.models.domain_models import IdeaAnalysis, PlaytestReview, ProjectState, PrototypeScope
from app.storage.fs_store import ensure_project_dirs, project_root
from app.storage.repositories.artifact_repo import ArtifactRepository
from app.storage.repositories.project_repo import ProjectRepository
from app.tools.file_tool import FileTool
from app.utils.ids import new_project_id


class ProjectService:
    def __init__(self) -> None:
        self.project_repo = ProjectRepository()
        self.artifact_repo = ArtifactRepository()

    def create_project(self, title: str, raw_idea: str, target_platform: str, target_engine: str) -> ProjectState:
        project_id = new_project_id()
        state = ProjectState(
            project_id=project_id,
            title=title or raw_idea[:40],
            raw_idea=raw_idea,
            target_platform=target_platform,
            target_engine=target_engine,
            current_stage=WorkflowStage.IDEA_RECEIVED,
            version=1,
        )
        ensure_project_dirs(project_id)
        self.project_repo.create(state)
        return state

    def get_project(self, project_id: str) -> ProjectState:
        return self.project_repo.get(project_id)

    def update_stage(self, project_id: str, stage: str) -> None:
        self.project_repo.update_stage(project_id, stage)

    def save_idea_analysis(self, project_id: str, analysis: IdeaAnalysis) -> Path:
        path = project_root(project_id) / "spec" / "idea_analysis.json"
        FileTool.write_json(path, analysis.model_dump())
        self.artifact_repo.add(project_id, str(path), "spec")
        return path

    def save_prototype_scope(self, project_id: str, scope: PrototypeScope) -> Path:
        path = project_root(project_id) / "spec" / "prototype_scope.json"
        FileTool.write_json(path, scope.model_dump())
        self.artifact_repo.add(project_id, str(path), "spec")
        return path

    def save_doc(self, project_id: str, name: str, content: str, kind: str = "doc") -> Path:
        path = project_root(project_id) / "docs" / name
        FileTool.write_text(path, content)
        self.artifact_repo.add(project_id, str(path), kind)
        return path

    def save_feedback_review(self, project_id: str, version: int, feedback_text: str, review: PlaytestReview) -> None:
        feedback_path = project_root(project_id) / "feedback" / f"feedback_v{version}.md"
        review_path = project_root(project_id) / "feedback" / f"review_v{version}.json"
        FileTool.write_text(feedback_path, feedback_text)
        FileTool.write_json(review_path, review.model_dump())
        self.artifact_repo.add(project_id, str(feedback_path), "feedback")
        self.artifact_repo.add(project_id, str(review_path), "feedback")

    def list_artifacts(self, project_id: str) -> list[str]:
        return self.artifact_repo.list_for_project(project_id)
