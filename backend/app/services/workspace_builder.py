from backend.app.agents.code_generator import CodeGenerator
from backend.app.models.workspace import Workspace


class WorkspaceBuilder:

    def __init__(self):
        self.generator = CodeGenerator()

    def _generate_in_batches(
        self,
        workspace: Workspace,
        file_paths: list[str],
        batch_size: int = 3
    ) -> dict[str, str]:

        generated_files = {}

        for start in range(
            0,
            len(file_paths),
            batch_size
        ):

            batch = file_paths[
                start:start + batch_size
            ]

            print(
                f"\n=== GENERATING BATCH "
                f"{start // batch_size + 1} ==="
            )

            for file_path in batch:
                print(f"Queued: {file_path}")

            result = self.generator.generate_batch(
                workspace,
                batch
            )

            for file_path, code in result.items():

                workspace.files[file_path] = code
                generated_files[file_path] = code

                print(
                    f"Generated: {file_path}"
                )

        return generated_files

    def build(
        self,
        workspace: Workspace
    ) -> Workspace:

        infrastructure_files = []
        core_files = []
        component_files = []
        page_files = []
        other_files = []

        for file_path in workspace.blueprint.files:

            if file_path in {
                "package.json",
                "vite.config.js",
                "tailwind.config.cjs",
                "postcss.config.cjs",
                "index.html",
                "src/index.css",
            }:
                infrastructure_files.append(
                    file_path
                )

            elif file_path in {
                "src/main.jsx",
                "src/App.jsx",
                "src/router.jsx",
            }:
                core_files.append(
                    file_path
                )

            elif "/components/" in file_path:
                component_files.append(
                    file_path
                )

            elif "/pages/" in file_path:
                page_files.append(
                    file_path
                )

            else:
                other_files.append(
                    file_path
                )

        print(
            "\n=== GENERATING INFRASTRUCTURE ==="
        )

        for file_path in infrastructure_files:

            print(
                f"Generating: {file_path}"
            )

            code = (
                self.generator.generate_file(
                    workspace,
                    file_path
                )
            )

            workspace.files[file_path] = code

        print(
            "\n=== GENERATING CORE FILES ==="
        )

        for file_path in core_files:

            print(
                f"Generating: {file_path}"
            )

            code = (
                self.generator.generate_file(
                    workspace,
                    file_path
                )
            )

            workspace.files[file_path] = code

        if component_files:

            print(
                "\n=== GENERATING COMPONENTS "
                "IN SMALL BATCHES ==="
            )

            self._generate_in_batches(
                workspace,
                component_files,
                batch_size=3
            )

        if page_files:

            print(
                "\n=== GENERATING PAGES "
                "IN SMALL BATCHES ==="
            )

            self._generate_in_batches(
                workspace,
                page_files,
                batch_size=2
            )

        if other_files:

            print(
                "\n=== GENERATING OTHER FILES ==="
            )

            for file_path in other_files:

                print(
                    f"Generating: {file_path}"
                )

                code = (
                    self.generator.generate_file(
                        workspace,
                        file_path
                    )
                )

                workspace.files[file_path] = code

        return workspace