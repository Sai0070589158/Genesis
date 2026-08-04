from backend.app.services.project_generator import ProjectGenerator

generator = ProjectGenerator()

blueprint = generator.generate(
    "Create a luxury hotel website with online booking."
)

print(blueprint.model_dump_json(indent=2))