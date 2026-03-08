"""Artifact repository."""

from app.storage.db import get_connection


class ArtifactRepository:
    def add(self, project_id: str, path: str, kind: str) -> None:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO artifacts (project_id, path, kind) VALUES (?, ?, ?)",
                (project_id, path, kind),
            )
            conn.commit()

    def list_for_project(self, project_id: str) -> list[str]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT path FROM artifacts WHERE project_id = ? ORDER BY id ASC",
                (project_id,),
            ).fetchall()
        return [r[0] for r in rows]
