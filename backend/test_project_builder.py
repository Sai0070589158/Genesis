from backend.app.models.workspace import Workspace
from backend.app.models.blueprint import Blueprint
from backend.app.services.project_builder import ProjectBuilder


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
        "src/pages"
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


builder = ProjectBuilder()

project_dir = builder.build(
    workspace,
    "genesis_demo"
)

print(f"\nProject created at: {project_dir}")