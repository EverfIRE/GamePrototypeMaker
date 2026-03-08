# GamePrototypeMaker

Game Prototype Validation Agent MVP for converting raw game ideas into scoped prototype plans,
scaffold generation, and feedback-driven iteration planning.

## Implemented MVP (Backend)

- FastAPI API endpoints for project lifecycle.
- Deterministic workflow orchestrator with strict stage transitions.
- Pydantic data contracts for project, analysis, scope, and review outputs.
- Filesystem + SQLite persistence for project state and artifact history.
- Template-based web scaffold generation with targeted TODO patching.

## Quick start

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000/docs`.

## One-command environment install

You can bootstrap the backend virtual environment with:

```bash
python backend/install_env.py
```

Optional flags:

```bash
python backend/install_env.py --python python3.10 --venv-dir backend/.venv
python backend/install_env.py --skip-install
```

