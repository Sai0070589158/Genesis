from backend.app.services.repair_agent import RepairAgent
from backend.app.models.workspace import Workspace
from backend.app.models.blueprint import Blueprint


blueprint = Blueprint(
    framework="React",
    bundler="Vite",
    styling="Tailwind CSS",
    router="React Router",
    pages=["Home"],
    components=["Navbar"],
    folders=[
        "src",
        "src/components"
    ],
    files=[
        "package.json",
        "vite.config.js",
        "src/App.jsx",
        "src/components/Navbar.jsx"
    ]
)


workspace = Workspace(
    blueprint=blueprint,
    files={
        "package.json": """
{
  "name": "test-project",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "build": "vite build"
  },
  "devDependencies": {
    "vite": "^7.0.0"
  }
}
""",
        "vite.config.js": """
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [react()]
});
"""
    }
)


error = """
Error: Cannot find module '@vitejs/plugin-react'
"""

agent = RepairAgent()

repaired_code = agent.repair(
    workspace,
    "vite.config.js",
    error
)

print("\n=== REPAIRED FILE ===")
print(repaired_code)