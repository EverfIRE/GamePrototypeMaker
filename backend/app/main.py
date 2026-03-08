"""FastAPI entrypoint."""

from fastapi import FastAPI

from app.api.routes_agent import router as agent_router
from app.api.routes_feedback import router as feedback_router
from app.api.routes_generation import router as generation_router
from app.api.routes_projects import router as projects_router
from app.core.config import settings
from app.storage.db import init_db

init_db()

app = FastAPI(title=settings.app_name)
app.include_router(projects_router)
app.include_router(agent_router)
app.include_router(generation_router)
app.include_router(feedback_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
