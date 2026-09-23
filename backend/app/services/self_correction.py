from pathlib import Path

from backend.app.models.workspace import Workspace

from backend.app.services.build_validator import BuildValidator
from backend.app.services.error_analyzer import ErrorAnalyzer
from backend.app.services.repair_agent import RepairAgent
from backend.app.services.file_writer import FileWriter


class SelfCorrectionService:

    def __init__(
        self,
        max_attempts: int = 3
    ):

        self.max_attempts = max_attempts

        self.validator = BuildValidator()

        self.analyzer = ErrorAnalyzer()

        self.repair_agent = RepairAgent()

        self.file_writer = FileWriter()

    def run(
        self,
        workspace: Workspace,
        project_dir: Path
    ):

        for attempt in range(
            1,
            self.max_attempts + 1
        ):

            print(
                f"\n=== BUILD ATTEMPT "
                f"{attempt}/{self.max_attempts} ==="
            )

            result = self.validator.validate(
                project_dir
            )

            if result["success"]:

                print(
                    "\n=== BUILD SUCCESS ==="
                )

                return {
                    "success": True,
                    "attempts": attempt,
                    "message":
                        "Project built successfully."
                }

            print(
                "\n=== BUILD FAILED ==="
            )

            analysis = self.analyzer.analyze(
                result
            )

            print(
                "\n=== ERROR ANALYSIS ==="
            )

            print(analysis)

            if not analysis["has_error"]:

                return {
                    "success": False,
                    "attempts": attempt,
                    "message": (
                        "Build failed but no "
                        "repairable error was "
                        "identified."
                    ),
                    "error": result["error"]
                }

            repair_action = analysis.get(
                "repair_action"
            )

            if repair_action:

                success = self._apply_repair_action(
                    workspace,
                    project_dir,
                    repair_action
                )

                if not success:

                    return {
                        "success": False,
                        "attempts": attempt,
                        "message": (
                            "The deterministic "
                            "repair could not "
                            "be applied."
                        ),
                        "error": result["error"]
                    }

                continue

            file_path = (
                analysis.get("repair_file")
                or analysis.get("file")
            )

            if not file_path:

                return {
                    "success": False,
                    "attempts": attempt,
                    "message": (
                        "Could not identify a "
                        "safe file to repair."
                    ),
                    "error": result["error"]
                }

            file_path = self._relative_file_path(
                project_dir,
                file_path
            )

            if self._is_protected_file(
                file_path
            ):

                print(
                    "\n=== PROTECTED FILE ==="
                )

                print(
                    f"Genesis will not modify: "
                    f"{file_path}"
                )

                return {
                    "success": False,
                    "attempts": attempt,
                    "message": (
                        "The detected error "
                        "belongs to a protected "
                        "dependency file."
                    ),
                    "error": result["error"]
                }

            if (
                file_path not in workspace.files
                and file_path != "index.html"
            ):

                return {
                    "success": False,
                    "attempts": attempt,
                    "message": (
                        f"Repair target "
                        f"'{file_path}' does not "
                        "exist in the workspace."
                    ),
                    "error": result["error"]
                }

            print(
                f"\n=== REPAIRING: "
                f"{file_path} ==="
            )

            repaired_code = (
                self.repair_agent.repair(
                    workspace,
                    file_path,
                    result["error"]
                )
            )

            workspace.files[file_path] = (
                repaired_code
            )

            self.file_writer.write(
                workspace,
                project_dir.name
            )

        return {
            "success": False,
            "attempts": self.max_attempts,
            "message":
                "Maximum repair attempts reached."
        }

    def _apply_repair_action(
        self,
        workspace: Workspace,
        project_dir: Path,
        action: dict
    ) -> bool:

        action_type = action.get(
            "type"
        )

        # ---------------------------------
        # RENAME
        # ---------------------------------

        if action_type == "rename":

            source = action["source"]

            destination = action[
                "destination"
            ]

            source_path = (
                project_dir / source
            )

            destination_path = (
                project_dir / destination
            )

            print(
                "\n=== REPAIR ACTION: RENAME ==="
            )

            print(
                f"{source} -> {destination}"
            )

            if not source_path.exists():

                print(
                    f"Source file does not exist: "
                    f"{source_path}"
                )

                return False

            if destination_path.exists():

                print(
                    f"Destination already exists: "
                    f"{destination_path}"
                )

                return False

            source_path.rename(
                destination_path
            )

            if source in workspace.files:

                workspace.files[
                    destination
                ] = workspace.files.pop(
                    source
                )

            return True

        # ---------------------------------
        # REWRITE
        # ---------------------------------

        if action_type == "rewrite":

            file_path = action.get(
                "file"
            )

            if not file_path:
                return False

            print(
                "\n=== REPAIR ACTION: "
                "REWRITE ==="
            )

            print(
                f"Rewriting: {file_path}"
            )

            if file_path == (
                "postcss.config.cjs"
            ):

                repaired_code = """module.exports = {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
"""

                workspace.files[
                    file_path
                ] = repaired_code

                self.file_writer.write(
                    workspace,
                    project_dir.name
                )

                return True

            return False

        return False

    def _relative_file_path(
        self,
        project_dir: Path,
        file_path: str
    ) -> str:

        project_dir = (
            project_dir.resolve()
        )

        path = Path(
            file_path
        )

        if not path.is_absolute():

            return file_path.replace(
                "\\",
                "/"
            )

        path = path.resolve()

        try:

            return str(
                path.relative_to(
                    project_dir
                )
            ).replace(
                "\\",
                "/"
            )

        except ValueError:

            return file_path.replace(
                "\\",
                "/"
            )

    def _is_protected_file(
        self,
        file_path: str
    ) -> bool:

        normalized = (
            file_path
            .replace("\\", "/")
            .lower()
        )

        protected_parts = [
            "node_modules/",
            ".git/",
            "package-lock.json"
        ]

        return any(
            part in normalized
            for part in protected_parts
        )