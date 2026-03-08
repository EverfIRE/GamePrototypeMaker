"""Targeted code patch helper."""

from pathlib import Path


class CodePatcher:
    @staticmethod
    def append_todo(path: Path, lines: list[str]) -> None:
        existing = path.read_text(encoding="utf-8") if path.exists() else ""
        content = existing + "\n" + "\n".join(f"// TODO: {line}" for line in lines) + "\n"
        path.write_text(content, encoding="utf-8")
