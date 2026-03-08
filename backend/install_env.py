#!/usr/bin/env python3
"""Bootstrap local Python environment for the backend project.

Usage:
  python backend/install_env.py
  python backend/install_env.py --python python3.10 --venv-dir backend/.venv
  python backend/install_env.py --skip-install
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print(f"[run] {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install backend dev environment")
    parser.add_argument("--python", default=sys.executable, help="Python interpreter used to create virtualenv")
    parser.add_argument("--venv-dir", default="backend/.venv", help="Virtual environment directory")
    parser.add_argument(
        "--requirements",
        default="backend/requirements.txt",
        help="Path to requirements.txt",
    )
    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="Only create venv and upgrade pip/setuptools/wheel",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    venv_dir = (repo_root / args.venv_dir).resolve()
    requirements = (repo_root / args.requirements).resolve()

    if not requirements.exists() and not args.skip_install:
        raise FileNotFoundError(f"Requirements file not found: {requirements}")

    venv_dir.parent.mkdir(parents=True, exist_ok=True)

    # 1) create venv
    run([args.python, "-m", "venv", str(venv_dir)])

    # 2) locate venv python executable
    if sys.platform.startswith("win"):
        venv_python = venv_dir / "Scripts" / "python.exe"
    else:
        venv_python = venv_dir / "bin" / "python"

    if not venv_python.exists():
        raise FileNotFoundError(f"Virtualenv python not found: {venv_python}")

    # 3) upgrade packaging tools
    run([str(venv_python), "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])

    # 4) install project dependencies
    if not args.skip_install:
        run([str(venv_python), "-m", "pip", "install", "-r", str(requirements)])

    print("\nEnvironment bootstrap complete.")
    print(f"Activate with: source {venv_dir}/bin/activate")
    print("Run API with: uvicorn app.main:app --reload --app-dir backend")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
