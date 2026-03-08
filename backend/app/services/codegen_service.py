"""Generate runnable skeleton via templates and targeted patches."""

from pathlib import Path

from app.models.domain_models import PrototypeScope
from app.tools.code_patcher import CodePatcher
from app.tools.template_loader import TemplateLoader


class CodegenService:
    def __init__(self) -> None:
        self.loader = TemplateLoader()

    def generate(self, generated_dir: Path, engine: str, scope: PrototypeScope) -> list[Path]:
        project_dir = self.loader.copy_engine_base(engine, generated_dir)
        main_script = project_dir / "src" / "game.js"
        CodePatcher.append_todo(
            main_script,
            [
                f"Implement prototype goal: {scope.prototype_goal}",
                *[f"Must-have feature: {feature}" for feature in scope.must_have],
            ],
        )
        return [project_dir, main_script]
