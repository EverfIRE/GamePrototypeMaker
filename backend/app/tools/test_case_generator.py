"""Build lightweight test checklist from prototype goal."""


def build_test_checklist(prototype_goal: str, metrics: list[str]) -> list[str]:
    checks = [f"Verify prototype goal can be completed: {prototype_goal}"]
    checks.extend(f"Measure metric: {metric}" for metric in metrics)
    return checks
