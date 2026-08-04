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
    "index.html",
    "src/main.jsx",
    "src/App.jsx",
    "src/components/Header.jsx",
    "src/pages/Home.jsx"
  ]
}}

Return JSON only.
"""

        response = self.llm.generate(prompt)

        data = json.loads(response)

        return Blueprint(**data)