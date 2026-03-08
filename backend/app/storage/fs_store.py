"""Filesystem helpers for project workspace layout."""

from pathlib import Path

from app.core.config import settings


def project_root(project_id: str) -> Path:
    return Path(settings.workspace_root) / project_id


def ensure_project_dirs(project_id: str) -> Path:
    root = project_root(project_id)
    for sub in ["spec", "docs", "generated", "feedback", "logs"]:
        (root / sub).mkdir(parents=True, exist_ok=True)
    return root
