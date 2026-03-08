from app.core.constants import WorkflowStage
from app.orchestrator.workflow import WorkflowOrchestrator


def test_stage_transition_progression() -> None:
    workflow = WorkflowOrchestrator()
    state = workflow.project_service.create_project(
        title="wf",
        raw_idea="minimal puzzle with chain reactions",
        target_platform="PC",
        target_engine="web",
    )
    workflow.analyze_idea(state.project_id)
    workflow.scope_prototype(state.project_id)
    stage = workflow.project_service.get_project(state.project_id).current_stage
    assert stage == WorkflowStage.PROTOTYPE_SCOPED
