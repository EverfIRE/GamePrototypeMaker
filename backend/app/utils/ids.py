"""ID utility functions."""

from uuid import uuid4


def new_project_id() -> str:
    return f"proj_{uuid4().hex[:10]}"
