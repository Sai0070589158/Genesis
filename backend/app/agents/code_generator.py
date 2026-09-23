from backend.app.llm.groq_provider import GroqProvider
from backend.app.models.workspace import Workspace


class CodeGenerator:

    def __init__(self):
        self.llm = GroqProvider()

    def generate_package_json(self) -> str:
        return """{
  "name": "genesis-generated-project",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router-dom": "^7.0.0"
  },
  "devDependencies": {
    "@tailwindcss/postcss": "^4.0.0",
    "@vitejs/plugin-react": "^5.0.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.5.0",
    "tailwindcss": "^4.0.0",
    "vite": "^7.0.0"
  }
}"""

    def generate_file(
        self,
        workspace: Workspace,
        file_path: str
    ) -> str:

        if file_path == "package.json":
            return self.generate_package_json()

        # Genesis controls these configuration files
        # deterministically instead of asking the LLM
        # to invent configuration.

        if file_path == "postcss.config.cjs":
            return """module.exports = {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
"""

        if file_path == "tailwind.config.cjs":
            return """module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
"""

        available_files = self._get_available_files(
            workspace,
            file_path
        )

        relevant_files = self._get_relevant_files(
            workspace,
            file_path
        )

        context = ""

        if relevant_files:
            context = "\n\n".join(
                f"--- {path} ---\n{workspace.files[path]}"
                for path in relevant_files
                if path in workspace.files
            )

        prompt = f"""
You are an expert React, Vite, and Tailwind CSS developer.

Generate the source code for exactly ONE file.

PROJECT:

Framework:
{workspace.blueprint.framework}

Bundler:
{workspace.blueprint.bundler}

Styling:
{workspace.blueprint.styling}

Router:
{workspace.blueprint.router}

PAGES:

{", ".join(workspace.blueprint.pages)}

COMPONENTS:

{", ".join(workspace.blueprint.components)}

ALL AVAILABLE PROJECT FILES:

{available_files}

FILE TO GENERATE:

{file_path}

RELEVANT EXISTING FILES:

{context}

IMPORTANT RULES:

1. Generate ONLY the contents of the requested file.
2. Do not use Markdown code fences.
3. Do not explain anything.
4. Follow the React + Vite + Tailwind CSS architecture.
5. Use correct relative imports.
6. Keep the code clean and production-ready.
7. Keep this file consistent with the relevant existing files.
8. Do not generate any other files.
9. All imports must refer to packages or files that exist.
10. React projects must use React and React DOM correctly.
11. React Router must be used when routing is defined.
12. Vite configuration must be compatible with package.json.
13. Do not introduce unnecessary dependencies.
14. Every imported npm package must exist in package.json.
15. Every local import must point to a file in the project.
16. Use JSX syntax for React components.
17. Use Tailwind CSS classes where appropriate.
18. Keep the application responsive.
19. Follow the pages and components defined in the blueprint.
20. Do not create fake binary content for image files.
21. If the requested file is CSS, return valid CSS only.
22. If the requested file is JSON, return valid JSON only.
23. If the requested file is JavaScript, return valid JavaScript only.
24. If the requested file is JSX, return valid JSX only.
25. Do not include Markdown formatting.
26. Do not introduce a new npm package unless it already exists in package.json.
27. Do not replace existing packages with alternative packages.
28. Preserve the project's existing technology choices.
29. Do not change Tailwind CSS configuration.
30. Do not change PostCSS configuration.
31. Use Tailwind CSS v4 syntax where applicable.

Return ONLY the file contents.
"""

        return self.llm.generate(prompt)

    def _get_available_files(
        self,
        workspace: Workspace,
        file_path: str
    ) -> str:

        files = workspace.blueprint.files

        return "\n".join(
            f"- {path}"
            for path in files
            if path != file_path
        )

    def _get_relevant_files(
        self,
        workspace: Workspace,
        file_path: str
    ) -> list[str]:

        relevant = []

        core_files = {
            "vite.config.js",
            "tailwind.config.cjs",
            "postcss.config.cjs",
            "src/main.jsx",
            "src/App.jsx",
            "src/router.jsx",
            "src/index.css",
            "src/styles/tailwind.css",
        }

        if (
            file_path.endswith(".config.js")
            or file_path.endswith(".config.cjs")
            or file_path in {
                "src/main.jsx",
                "src/App.jsx",
                "src/router.jsx",
                "index.html",
            }
        ):
            relevant.extend(core_files)

        if (
            "/components/" in file_path
            or "/pages/" in file_path
        ):
            relevant.extend([
                "src/App.jsx",
                "src/router.jsx",
                "src/main.jsx",
            ])

        result = []

        for path in relevant:
            if (
                path != file_path
                and path not in result
                and path in workspace.files
            ):
                result.append(path)

        return result[:5]