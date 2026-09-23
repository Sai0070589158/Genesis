from pathlib import Path

from backend.app.models.workspace import Workspace


class FileWriter:

    def write(self, workspace: Workspace, project_name: str) -> Path:

        project_dir = Path("generated_projects") / project_name

        project_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # Create all folders defined by the blueprint.
        for folder in workspace.blueprint.folders:

            folder_path = project_dir / folder

            folder_path.mkdir(
                parents=True,
                exist_ok=True
            )

        # Write generated files.
        for file_path, code in workspace.files.items():

            destination = project_dir / file_path

            # Prevent a directory from being treated as a file.
            if destination.exists() and destination.is_dir():
                print(f"Skipping directory listed as file: {file_path}")
                continue

            destination.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            destination.write_text(
                code,
                encoding="utf-8"
            )

            print(f"Written: {destination}")

        return project_dir