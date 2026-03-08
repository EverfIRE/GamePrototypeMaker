"""Application configuration."""

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Game Prototype Validation Agent"
    workspace_root: str = "workspace/projects"
    database_path: str = "backend/app/storage/db/sqlite.db"


settings = Settings()
