from backend.app.models.workspace import Workspace
from backend.app.models.blueprint import Blueprint
from backend.app.services.file_writer import FileWriter


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
        "src/pages/Home.jsx"
    ]
)


workspace = Workspace(
    blueprint=blueprint,
    files={
        "src/App.jsx": "export default function App() { return <h1>Hello Genesis</h1>; }",
        "src/components/Navbar.jsx": "export default function Navbar() { return <nav>Navbar</nav>; }",
        "src/pages/Home.jsx": "export default function Home() { return <h1>Home</h1>; }"
    }
)


writer = FileWriter()

project_dir = writer.write(
    workspace,
    "test_project"
)

print(f"\nProject created at: {project_dir}")