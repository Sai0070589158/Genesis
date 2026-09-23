import shutil
from pathlib import Path

from backend.app.models.workspace import Workspace
from backend.app.models.blueprint import Blueprint
from backend.app.services.self_correction import SelfCorrectionService

# ============================================================
# TEST BLUEPRINT
# ============================================================

blueprint = Blueprint(
    framework="React",
    bundler="Vite",
    styling="Tailwind CSS",
    router="React Router",
    pages=["Home"],
    components=["Navbar"],
    folders=[
        "src",
        "src/components",
    ],
    files=[
        "package.json",
        "vite.config.js",
        "index.html",
        "src/main.jsx",
        "src/App.jsx",
        "src/components/Navbar.jsx",
    ],
)


# ============================================================
# TEST WORKSPACE
# ============================================================

workspace = Workspace(
    blueprint=blueprint,

    files={

        # ----------------------------------------------------
        # Deliberately broken package.json
        #
        # @vitejs/plugin-react is missing.
        # This gives Genesis a real build error to repair.
        # ----------------------------------------------------

        "package.json": """{
  "name": "genesis-self-correction-test",
  "version": "1.0.0",
  "private": true,
  "type": "module",

  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },

  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },

  "devDependencies": {
    "vite": "^7.0.0"
  }
}""",

        # ----------------------------------------------------
        # Vite configuration
        #
        # This imports @vitejs/plugin-react, but the package
        # is intentionally missing from package.json.
        # ----------------------------------------------------

        "vite.config.js": """import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
    plugins: [react()]
});
""",

        # ----------------------------------------------------
        # Vite entry page
        # ----------------------------------------------------

        "index.html": """<!doctype html>
<html lang="en">

<head>
    <meta charset="UTF-8" />

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    />

    <title>Genesis Test</title>
</head>

<body>

    <div id="root"></div>

    <script
        type="module"
        src="/src/main.jsx"
    ></script>

</body>

</html>
""",

        # ----------------------------------------------------
        # React entry point
        # ----------------------------------------------------

        "src/main.jsx": """import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App.jsx";


ReactDOM.createRoot(
    document.getElementById("root")
).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
""",

        # ----------------------------------------------------
        # Main application
        # ----------------------------------------------------

        "src/App.jsx": """import Navbar from "./components/Navbar.jsx";


export default function App() {

    return (
        <>
            <Navbar />

            <main>
                <h1>Hello Genesis</h1>
                <p>
                    This project is testing
                    Genesis self-correction.
                </p>
            </main>
        </>
    );
}
""",

        # ----------------------------------------------------
        # Navbar component
        # ----------------------------------------------------

        "src/components/Navbar.jsx": """export default function Navbar() {

    return (
        <nav>
            <h2>Genesis</h2>
        </nav>
    );
}
""",
    }
)


# ============================================================
# CREATE TEST PROJECT DIRECTORY
# ============================================================
project_dir = Path(
    "generated_projects/self_correction_test"
)

# Delete the previous test project completely
if project_dir.exists():
    shutil.rmtree(project_dir)

# Create a fresh test project
project_dir.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# WRITE INITIAL TEST PROJECT
# ============================================================

print("\n=== CREATING TEST PROJECT ===")

for file_path, code in workspace.files.items():

    destination = project_dir / file_path

    destination.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    destination.write_text(
        code,
        encoding="utf-8"
    )

    print(f"Created: {destination}")


print(
    f"\nTest project created at: {project_dir}"
)


# ============================================================
# RUN SELF-CORRECTION
# ============================================================

print("\n=== STARTING SELF-CORRECTION ===")

service = SelfCorrectionService(
    max_attempts=3
)

result = service.run(
    workspace,
    project_dir
)


# ============================================================
# FINAL RESULT
# ============================================================

print("\n=== FINAL RESULT ===")

print(result)