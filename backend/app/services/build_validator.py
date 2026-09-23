import subprocess
from pathlib import Path


class BuildValidator:

    def install_dependencies(self, project_dir: Path):

        print("\n=== Installing dependencies ===")

        return subprocess.run(
            ["npm.cmd", "install"],
            cwd=project_dir,
            capture_output=True,
            text=True
        )

    def build(self, project_dir: Path):

        print("\n=== Building project ===")

        return subprocess.run(
            ["npm.cmd", "run", "build"],
            cwd=project_dir,
            capture_output=True,
            text=True
        )

    def validate(self, project_dir: Path):

        install_result = self.install_dependencies(project_dir)

        if install_result.returncode != 0:

            return {
                "success": False,
                "stage": "npm install",
                "output": install_result.stdout,
                "error": install_result.stderr
            }

        build_result = self.build(project_dir)

        if build_result.returncode != 0:

            return {
                "success": False,
                "stage": "npm run build",
                "output": build_result.stdout,
                "error": build_result.stderr
            }

        return {
            "success": True,
            "stage": "build",
            "output": build_result.stdout,
            "error": ""
        }