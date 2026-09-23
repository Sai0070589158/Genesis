from backend.app.agents.code_generator import CodeGenerator
from backend.app.models.workspace import Workspace
from backend.app.models.blueprint import Blueprint
from backend.app.services.workspace_builder import WorkspaceBuilder


blueprint = Blueprint(
    framework="React",
    bundler="Vite",
    styling="Tailwind CSS",
    router="React Router",
    pages=[
        "Home",
        "About"
    ],
    components=[
        "Navbar",
        "Footer"
    ],
    folders=[
        "src",
        "src/components",
        "src/pages",
        "src/styles",
        "public"
    ],
    files=[
        "src/App.jsx",
        "src/components/Navbar.jsx",
        "src/components/Footer.jsx",
        "src/pages/Home.jsx",
        "src/pages/About.jsx"
    ]
)


workspace = Workspace(
    blueprint=blueprint,
    files={}
)


builder = WorkspaceBuilder()

workspace = builder.build(workspace)

print("\nGenerated files:\n")

for file_path in workspace.files:
    print(file_path)