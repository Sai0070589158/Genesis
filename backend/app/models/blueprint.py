from pydantic import BaseModel


class Blueprint(BaseModel):
    framework: str
    bundler: str
    styling: str
    router: str

    pages: list[str]
    components: list[str]

    folders: list[str]
    files: list[str]