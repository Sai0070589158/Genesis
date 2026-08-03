import json

from backend.app.llm.groq_provider import GroqProvider
from backend.app.models.project_spec import ProjectSpec
from backend.app.models.website_plan import WebsitePlan


class Developer:

    def __init__(self):
        self.llm = GroqProvider()

    def generate_project(self, plan: WebsitePlan) -> ProjectSpec:

        prompt = f"""
You are a senior React architect.

Given this website plan:

{plan.model_dump_json(indent=2)}

Return ONLY valid JSON.

Format:

{{
    "framework":"React",
    "bundler":"Vite",
    "styling":"Tailwind CSS",
    "pages":[],
    "components":[]
}}
"""

        response = self.llm.generate(prompt)

        data = json.loads(response)

        return ProjectSpec(**data)