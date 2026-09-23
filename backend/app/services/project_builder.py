from pathlib import Path

from backend.app.models.workspace import Workspace
from backend.app.services.workspace_builder import WorkspaceBuilder
from backend.app.services.file_writer import FileWriter


class ProjectBuilder:

    def __init__(self):
        self.workspace_builder = WorkspaceBuilder()
        self.file_writer = FileWriter()

    def build(self, workspace: Workspace, project_name: str) -> Path:

        print("\n=== Generating project files ===")

        workspace = self.workspace_builder.build(workspace)

        print("\n=== Writing project files ===")

        project_dir = self.file_writer.write(
            workspace,
            project_name
        )

        return project_dir