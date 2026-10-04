import json

from backend.app.llm.groq_provider import GroqProvider
from backend.app.models.blueprint import Blueprint
from backend.app.models.project_spec import ProjectSpec


class Architect:

    def __init__(self):
        self.llm = GroqProvider()

    def design(self, spec: ProjectSpec) -> Blueprint:

        prompt = f"""
You are an expert React + Vite software architect.

Given this project specification:

{spec.model_dump_json(indent=2)}

Design a COMPLETE React project.

Return ONLY valid JSON.

Rules:

1. Use React.
2. Use Vite.
3. Use Tailwind CSS.
4. Use React Router.
5. Every page must have its own JSX file.
6. Every component must have its own JSX file.
7. Return complete folder paths.
8. Return complete file paths.
9. Every item in "files" must represent an actual file.
10. Every file must have a filename with an appropriate extension.
11. Never put directory paths in the "files" array.
12. Paths such as "src/assets/images" and "src/assets/fonts" are folders, not files.
13. If assets directories are required, put them in the "folders" array.
14. Do not create placeholder files for empty directories.

Infrastructure files must use exactly these names:

- package.json
- vite.config.js
- tailwind.config.cjs
- postcss.config.cjs
- index.html
- src/main.jsx
- src/App.jsx
- src/router.jsx
- src/index.css

Do not use:
- tailwind.config.js
- postcss.config.js

Example output:

{{
  "framework": "React",
  "bundler": "Vite",
  "styling": "Tailwind CSS",
  "router": "React Router",
  "pages": ["Home"],
  "components": ["Header"],
  "folders": [
    "src",
    "src/components",
    "src/pages",
    "src/assets",
    "src/styles",
    "public"
  ],
  "files": [
    "package.json",
    "vite.config.js",
    "tailwind.config.cjs",
    "postcss.config.cjs",
    "index.html",
    "src/main.jsx",
    "src/App.jsx",
    "src/router.jsx",
    "src/index.css",
    "src/components/Header.jsx",
    "src/pages/Home.jsx"
  ]
}}

Return JSON only.
"""

        response = self.llm.generate(prompt)

        data = json.loads(response)

        data = self._normalize_infrastructure_files(data)

        return Blueprint(**data)

    def _normalize_infrastructure_files(
        self,
        data: dict
    ) -> dict:

        files = data.get("files", [])

        normalized_files = []

        for file_path in files:

            if file_path == "tailwind.config.js":
                file_path = "tailwind.config.cjs"

            elif file_path == "postcss.config.js":
                file_path = "postcss.config.cjs"

            if file_path not in normalized_files:
                normalized_files.append(file_path)

        required_files = [
            "package.json",
            "vite.config.js",
            "tailwind.config.cjs",
            "postcss.config.cjs",
            "index.html",
            "src/main.jsx",
            "src/App.jsx",
            "src/router.jsx",
            "src/index.css",
        ]

        for required_file in required_files:
            if required_file not in normalized_files:
                normalized_files.append(required_file)

        data["files"] = normalized_files

        return data