"""Project repository for SQLite-backed project states."""

from app.models.domain_models import ProjectState
from app.storage.db import get_connection


class ProjectRepository:
    def create(self, state: ProjectState) -> None:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO projects (project_id, title, raw_idea, target_platform, target_engine, current_stage, version)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    state.project_id,
                    state.title,
                    state.raw_idea,
                    state.target_platform,
                    state.target_engine,
                    state.current_stage,
                    state.version,
                ),
            )
            conn.commit()

    def update_stage(self, project_id: str, stage: str) -> None:
        with get_connection() as conn:
            conn.execute(
                "UPDATE projects SET current_stage = ? WHERE project_id = ?",
                (stage, project_id),
            )
            conn.commit()

    def get(self, project_id: str) -> ProjectState:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT project_id, title, raw_idea, target_platform, target_engine, current_stage, version FROM projects WHERE project_id = ?",
                (project_id,),
            ).fetchone()
        if row is None:
            raise ValueError(f"Project not found: {project_id}")
        return ProjectState(
            project_id=row[0],
            title=row[1],
            raw_idea=row[2],
            target_platform=row[3],
            target_engine=row[4],
            current_stage=row[5],
            version=row[6],
        )
