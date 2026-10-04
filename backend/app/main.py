from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

from backend.app.services.project_generator import ProjectGenerator
from backend.app.services.workspace_builder import WorkspaceBuilder
from backend.app.services.file_writer import FileWriter
from backend.app.services.self_correction import SelfCorrectionService


app = FastAPI(
    title="Genesis API",
    version="1.0.0"
)

generator = ProjectGenerator()
workspace_builder = WorkspaceBuilder()
file_writer = FileWriter()
self_correction = SelfCorrectionService(max_attempts=3)


class WebsiteRequest(BaseModel):
    prompt: str


@app.get("/")
def home():
    return {"message": "Welcome to Genesis 🚀"}


@app.post("/generate")
def generate(request: WebsiteRequest):

    # 1. Generate project architecture
    workspace = generator.generate(request.prompt)

    # 2. Generate all project files
    workspace = workspace_builder.build(workspace)

    # 3. Write project to disk
    project_name = "genesis_generated"

    project_dir = file_writer.write(
        workspace,
        project_name
    )

    project_dir = Path(project_dir)

    # 4. Validate build and automatically repair errors
    correction_result = self_correction.run(
        workspace,
        project_dir
    )

    return {
        "status": "success"
        if correction_result["success"]
        else "failed",
        "project": project_name,
        "project_path": str(project_dir),
        "build": correction_result,
        "blueprint": workspace.blueprint.model_dump(),
        "files": list(workspace.files.keys())
    }