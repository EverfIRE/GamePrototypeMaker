"""Code builder agent."""

from pathlib import Path

from app.models.domain_models import PrototypeScope
from app.services.codegen_service import CodegenService


class CodeBuilder:
    def __init__(self, codegen_service: CodegenService) -> None:
        self.codegen_service = codegen_service

    def run(self, generated_dir: Path, engine: str, scope: PrototypeScope) -> list[Path]:
        return self.codegen_service.generate(generated_dir, engine, scope)
