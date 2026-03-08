"""Feedback repository."""

import json

from app.models.domain_models import PlaytestReview
from app.storage.db import get_connection


class FeedbackRepository:
    def add(self, project_id: str, version: int, feedback_text: str, review: PlaytestReview) -> None:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO feedback (project_id, version, feedback_text, review_json) VALUES (?, ?, ?, ?)",
                (project_id, version, feedback_text, json.dumps(review.model_dump())),
            )
            conn.commit()
