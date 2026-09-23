from backend.app.agents.code_generator import CodeGenerator
from backend.app.models.workspace import Workspace


class RepairAgent:

    def __init__(self):
        self.generator = CodeGenerator()

    def repair(
        self,
        workspace: Workspace,
        file_path: str,
        error: str
    ) -> str:

        current_code = workspace.files.get(
            file_path,
            ""
        )

        # Keep the build error small enough
        # for the LLM context window / TPM limit.
        error_context = error[-5000:]

        prompt = f"""
You are an expert React, Vite, Tailwind CSS, and PostCSS debugging engineer.

A generated web project failed during its build.

Your job is to repair exactly ONE file.

TARGET FILE:
{file_path}

CURRENT FILE CONTENT:
{current_code}

BUILD ERROR:
{error_context}

PROJECT TECHNOLOGY:
Framework: {workspace.blueprint.framework}
Bundler: {workspace.blueprint.bundler}
Styling: {workspace.blueprint.styling}
Router: {workspace.blueprint.router}

RULES:

1. Return ONLY the corrected contents of the target file.
2. Do not use Markdown code fences.
3. Do not explain the solution.
4. Fix the ROOT CAUSE of the build error.
5. Never hide, suppress, bypass, or ignore a build error.
6. Never create a fake fallback for a missing dependency.
7. Never use try/catch to hide missing npm packages.
8. Do not introduce unnecessary dependencies.
9. Do not modify unrelated functionality.
10. Preserve the existing project architecture.
11. Keep the file compatible with the existing React and Vite versions.
12. If repairing package.json, preserve existing dependency versions unless the build error explicitly requires a dependency change.
13. Only add a dependency when the build error explicitly indicates that the dependency is missing or required.
14. Never replace an existing dependency with a different package unless the build error explicitly requires that replacement.
15. Never arbitrarily downgrade a package.
16. Never modify node_modules.
17. Never use --force or --legacy-peer-deps.
18. If repairing package.json, return valid JSON only.
19. Do not change unrelated dependencies.
20. Do not change the project's framework or bundler.
21. Return valid source code only.

IMPORTANT:

If the error is caused by a missing npm dependency, update package.json only when package.json is the requested target.

If the error does not require changing a dependency, preserve the existing dependencies exactly.

Return ONLY the corrected file contents.
"""

        repaired_code = self.generator.llm.generate(
            prompt
        )

        repaired_code = self._clean_response(
            repaired_code
        )

        workspace.files[file_path] = repaired_code

        return repaired_code

    def _clean_response(self, code: str) -> str:

        code = code.strip()

        if code.startswith("```"):

            lines = code.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            code = "\n".join(lines).strip()

        return code