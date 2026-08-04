from pydantic import BaseModel

from backend.app.models.blueprint import Blueprint


class Workspace(BaseModel):
    blueprint: Blueprint
    files: dict[str, str] = {}