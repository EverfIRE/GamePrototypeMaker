"""Loads and copies template projects."""

import shutil
from pathlib import Path


class TemplateLoader:
    def __init__(self, templates_root: str = "backend/app/templates") -> None:
        self.templates_root = Path(templates_root)

    def copy_engine_base(self, engine: str, destination: Path) -> Path:
        if engine != "web":
            raise ValueError("MVP currently supports only web engine")
        src = self.templates_root / "web" / "phaser_base"
        if not src.exists():
            raise FileNotFoundError(f"Missing engine template at {src}")
        target = destination / "web_project"
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(src, target)
        return target
