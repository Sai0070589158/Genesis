from backend.app.agents.code_generator import CodeGenerator
from backend.app.models.workspace import Workspace


class WorkspaceBuilder:

    def __init__(self):
        self.generator = CodeGenerator()

    def build(self, workspace: Workspace) -> Workspace:

        for file_path in workspace.blueprint.files:

            print(f"Generating: {file_path}")

            code = self.generator.generate_file(
                workspace,
                file_path
            )

            workspace.files[file_path] = code

        return workspace