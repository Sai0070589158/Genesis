from backend.app.agents.planner import Planner
from backend.app.agents.developer import Developer
from backend.app.agents.architect import Architect
from backend.app.models.workspace import Workspace


class ProjectGenerator:

    def __init__(self):
        self.planner = Planner()
        self.developer = Developer()
        self.architect = Architect()

    def generate(self, prompt: str):

        plan = self.planner.plan(prompt)

        spec = self.developer.generate_project(plan)

        blueprint = self.architect.design(spec)

        return Workspace(
    blueprint=blueprint,
    files={}
)