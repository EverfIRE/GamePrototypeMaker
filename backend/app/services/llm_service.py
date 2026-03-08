"""LLM service abstraction.

MVP uses deterministic heuristics so the workflow remains testable.
"""

from app.models.domain_models import IdeaAnalysis, PlaytestReview, PrototypeScope


class LLMService:
    def analyze_idea(self, raw_idea: str) -> IdeaAnalysis:
        trimmed = raw_idea.strip()
        return IdeaAnalysis(
            game_pitch=f"A focused prototype for: {trimmed}",
            player_goal="Survive and achieve a clear short objective in one session.",
            core_loop=["Observe state", "Take action", "Receive feedback", "Adjust strategy"],
            fun_hypotheses=["Players enjoy quick strategic decisions", "Core action feels responsive"],
            risks=["Core loop may feel repetitive", "Difficulty ramp may spike too early"],
            inspirations=[],
        )

    def scope_prototype(self, analysis: IdeaAnalysis) -> PrototypeScope:
        return PrototypeScope(
            prototype_goal=f"Validate the main fun loop of: {analysis.game_pitch}",
            must_have=[
                "Single playable level",
                "Player input and movement/action",
                "Win or lose condition within 3-5 minutes",
            ],
            should_cut=["Progression meta systems", "Online multiplayer", "Final art polish"],
            nice_to_have=["Basic sound effects", "Simple restart flow"],
            success_metrics=[
                "At least 70% testers understand goal in 30 seconds",
                "At least 60% testers replay one more round",
            ],
        )

    def review_playtest(self, feedback_text: str, current_goal: str) -> PlaytestReview:
        return PlaytestReview(
            issues=[feedback_text],
            root_causes=["Onboarding and balancing are underdefined in prototype scope"],
            priority_changes=["Improve first-minute tutorial cues", "Flatten early difficulty curve"],
            next_experiments=[f"Run focused test on onboarding clarity for goal: {current_goal}"],
        )
