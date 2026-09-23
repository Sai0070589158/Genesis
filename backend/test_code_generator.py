from backend.app.agents.code_generator import CodeGenerator
from backend.app.models.workspace import Workspace
from backend.app.models.blueprint import Blueprint


blueprint = Blueprint(
    framework="React",
    bundler="Vite",
    styling="Tailwind CSS",
    router="React Router",
    pages=["Home", "About", "Contact"],
    components=["Navbar", "Hero", "Footer"],
    folders=[
        "src",
        "src/components",
        "src/pages",
        "src/styles",
        "public"
    ],
    files=[
        "package.json",
        "index.html",
        "src/main.jsx",
        "src/App.jsx",
        "src/components/Navbar.jsx",
        "src/components/Hero.jsx",
        "src/components/Footer.jsx",
        "src/pages/Home.jsx",
        "src/pages/About.jsx",
        "src/pages/Contact.jsx"
    ]
)


workspace = Workspace(
    blueprint=blueprint,
    files={}
)


generator = CodeGenerator()

code = generator.generate_file(
    workspace,
    "src/components/Navbar.jsx"
)

print(code)