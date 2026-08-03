from pydantic import BaseModel


class ProjectSpec(BaseModel):
    framework: str
    bundler: str
    styling: str
    pages: list[str]
    components: list[str]