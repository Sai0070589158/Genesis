import shutil
from pathlib import Path

from backend.app.agents.planner import Planner
from backend.app.agents.developer import Developer
from backend.app.agents.architect import Architect

from backend.app.models.workspace import Workspace

from backend.app.services.workspace_builder import WorkspaceBuilder
from backend.app.services.file_writer import FileWriter
from backend.app.services.self_correction import SelfCorrectionService


prompt = """

Create a modern portfolio website for a software developer.

It should have Home, About, Projects, and Contact pages.

Use a clean modern design with responsive layout and subtle animations.

"""


print("\n=== PLANNING ===")

planner = Planner()

plan = planner.plan(prompt)

print(
    plan.model_dump_json(
        indent=2
    )
)


print("\n=== DEVELOPMENT SPECIFICATION ===")

developer = Developer()

spec = developer.generate_project(
    plan
)

print(
    spec.model_dump_json(
        indent=2
    )
)


print("\n=== ARCHITECTURE ===")

architect = Architect()

blueprint = architect.design(
    spec
)

print(
    blueprint.model_dump_json(
        indent=2
    )
)


print("\n=== WORKSPACE ===")

workspace = Workspace(
    blueprint=blueprint,
    files={}
)

builder = WorkspaceBuilder()

workspace = builder.build(
    workspace
)


print("\n=== WRITING PROJECT ===")

# Always start with a clean generated project.
# This prevents stale files from previous generations
# from interfering with the current project.

project_root = Path(
    "generated_projects/genesis_portfolio"
)

if project_root.exists():

    print(
        "\n=== CLEANING PREVIOUS PROJECT ==="
    )

    shutil.rmtree(
        project_root
    )


writer = FileWriter()

project_dir = writer.write(
    workspace,
    "genesis_portfolio"
)

print(
    f"\nProject created at: {project_dir}"
)


print(
    "\n=== SELF-CORRECTION / BUILD VALIDATION ==="
)

service = SelfCorrectionService(
    max_attempts=3
)

result = service.run(
    workspace,
    project_dir
)


print(
    "\n=== FINAL BUILD RESULT ==="
)

print(result)