import json

from backend.app.llm.groq_provider import GroqProvider
from backend.app.models.project_spec import ProjectSpec
from backend.app.models.website_plan import WebsitePlan


class Developer:

    def __init__(self):
        self.llm = GroqProvider()

    def generate_project(self, plan: WebsitePlan) -> ProjectSpec:

        prompt = f"""
You are an expert frontend developer.

Convert the following website plan into a technical project specification.

Website Plan:
{plan.model_dump_json(indent=2)}

Return ONLY valid JSON.

The JSON must contain exactly these fields:

{{
  "framework": "React",
  "bundler": "Vite",
  "styling": "Tailwind CSS",
  "pages": [],
  "components": []
}}

Rules:

1. Return valid JSON only.
2. Do not use Markdown code fences.
3. Do not add explanations.
4. Use React as the framework.
5. Use Vite as the bundler.
6. Use Tailwind CSS for styling.
7. List all required pages.
8. List reusable components required by the website.
9. Use simple JSON strings.
10. Do not put raw newlines inside JSON strings.
11. Do not put tabs or control characters inside JSON strings.
"""

        response = self.llm.generate(prompt)

        # Remove accidental Markdown fences if the model adds them.
        response = response.strip()

        if response.startswith("```"):
            response = response.replace("```json", "", 1)
            response = response.replace("```", "", 1)
            response = response.strip()

        try:
            data = json.loads(response)

        except json.JSONDecodeError as error:
            print("\n=== INVALID DEVELOPER RESPONSE ===")
            print(response)
            print("\n=== JSON ERROR ===")
            print(error)
            raise

        return ProjectSpec(**data)