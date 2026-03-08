"""Validation utilities for workflow stages."""

from pathlib import Path


class ValidationService:
    @staticmethod
    def require_files(paths: list[Path]) -> None:
        missing = [str(p) for p in paths if not p.exists()]
        if missing:
            raise ValueError(f"Missing required files: {missing}")

    @staticmethod
    def validate_transition(current_stage: str, next_stage: str, transitions: dict[str, list[str]]) -> None:
        allowed = transitions.get(current_stage, [])
        if next_stage not in allowed:
            raise ValueError(f"Invalid transition {current_stage} -> {next_stage}")
