"""Domain contracts for structured workflow outputs."""

from pydantic import BaseModel, Field


class ProjectState(BaseModel):
    project_id: str
    title: str
    raw_idea: str
    target_platform: str
    target_engine: str
    current_stage: str
    version: int = 1


class IdeaAnalysis(BaseModel):
    game_pitch: str
    player_goal: str
    core_loop: list[str] = Field(min_length=1)
    fun_hypotheses: list[str] = Field(min_length=1)
    risks: list[str] = Field(min_length=1)
    inspirations: list[str] = []


class PrototypeScope(BaseModel):
    prototype_goal: str
    must_have: list[str] = Field(min_length=1)
    should_cut: list[str]
    nice_to_have: list[str]
    success_metrics: list[str] = Field(min_length=1)


class PlaytestReview(BaseModel):
    issues: list[str] = Field(min_length=1)
    root_causes: list[str] = Field(min_length=1)
    priority_changes: list[str] = Field(min_length=1)
    next_experiments: list[str] = Field(min_length=1)
