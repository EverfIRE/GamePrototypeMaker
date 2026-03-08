"""Generate docs artifacts from structured inputs."""

import json

from app.models.domain_models import IdeaAnalysis, PrototypeScope
from app.tools.test_case_generator import build_test_checklist


class DocService:
    def build_prototype_brief(self, idea: IdeaAnalysis, scope: PrototypeScope) -> str:
        return (
            f"# Prototype Brief\n\n"
            f"## Pitch\n{idea.game_pitch}\n\n"
            f"## Player Goal\n{idea.player_goal}\n\n"
            f"## Prototype Goal\n{scope.prototype_goal}\n\n"
            f"## Must Have\n" + "\n".join(f"- {x}" for x in scope.must_have) + "\n"
        )

    def build_test_plan(self, scope: PrototypeScope) -> str:
        checks = build_test_checklist(scope.prototype_goal, scope.success_metrics)
        return "# Test Plan\n\n" + "\n".join(f"- {c}" for c in checks) + "\n"

    def build_feature_list_json(self, scope: PrototypeScope) -> str:
        payload = {
            "must_have": scope.must_have,
            "should_cut": scope.should_cut,
            "nice_to_have": scope.nice_to_have,
        }
        return json.dumps(payload, indent=2)
