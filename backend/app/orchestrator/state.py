"""Workflow state definitions and transitions."""

from app.core.constants import WorkflowStage


VALID_TRANSITIONS: dict[str, list[str]] = {
    WorkflowStage.IDEA_RECEIVED: [WorkflowStage.IDEA_ANALYZED],
    WorkflowStage.IDEA_ANALYZED: [WorkflowStage.PROTOTYPE_SCOPED],
    WorkflowStage.PROTOTYPE_SCOPED: [WorkflowStage.DOC_GENERATED],
    WorkflowStage.DOC_GENERATED: [WorkflowStage.CODE_GENERATED],
    WorkflowStage.CODE_GENERATED: [WorkflowStage.PLAYTEST_REVIEWED],
    WorkflowStage.PLAYTEST_REVIEWED: [WorkflowStage.NEXT_ITERATION_PLANNED],
    WorkflowStage.NEXT_ITERATION_PLANNED: [],
}
