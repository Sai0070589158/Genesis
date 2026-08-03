# Genesis

> **AI Software Engineer for Autonomous Website Generation & Deployment**

Genesis is an AI-powered software engineering platform that transforms natural language prompts into complete, production-ready websites. Rather than generating everything with a single prompt, Genesis uses a modular multi-agent architecture where each AI agent is responsible for a specific stage of the software development lifecycle.

The long-term vision is to create an autonomous AI software engineer capable of understanding requirements, planning architecture, generating source code, validating projects, fixing errors, and deploying websites to GitHub Pages.

---

# 🚀 Features

- 🤖 Multi-Agent AI Architecture
- 🧠 AI Planner Agent
- 👨‍💻 AI Developer Agent
- ⚛️ React + Vite Project Generation
- 🎨 Tailwind CSS Support
- 📁 Automatic Project Structure Generation
- 🏗 Modular Backend Architecture
- 🔌 LLM Provider Abstraction Layer
- 🌐 GitHub Repository Creation *(Upcoming)*
- 🚀 GitHub Pages Deployment *(Upcoming)*
- 🔄 AI Website Editing *(Upcoming)*

---

# 🚧 Project Status

Genesis is currently under active development.

## ✅ Completed

- FastAPI Backend
- REST API
- Groq Integration
- LLM Provider Layer
- Planner Agent
- Developer Agent
- Website Planning
- Project Specification Generation

## 🚧 In Progress

- Architect Agent

## 📅 Planned

- Code Generator
- File Writer
- Project Validator
- Automatic Error Fixing
- GitHub Repository Publisher
- GitHub Pages Deployment
- AI Website Editing

---

# 🏗 System Architecture

```
                    User Prompt
                         │
                         ▼
                 Planner Agent
                         │
                         ▼
                  Website Plan
                         │
                         ▼
                Developer Agent
                         │
                         ▼
                 Project Specification
                         │
                         ▼
                 Architect Agent
                         │
                         ▼
                   Project Structure
                         │
                         ▼
                  Code Generator
                         │
                         ▼
                    File Writer
                         │
                         ▼
                   React Project
                         │
                         ▼
                    Build Validator
                         │
                         ▼
                  Automatic Fixes
                         │
                         ▼
                 GitHub Publisher
                         │
                         ▼
                 GitHub Pages
```

---

# 🧠 Multi-Agent Architecture

Genesis follows an agent-based architecture where each AI agent has a dedicated responsibility.

### Planner Agent

Responsible for understanding the user's prompt and creating a structured website plan.

Example output:

```json
{
  "website_type": "Hotel",
  "pages": [
    "Home",
    "Rooms",
    "Booking",
    "Contact"
  ],
  "theme": "Luxury",
  "color_scheme": [
    "#111827",
    "#D4AF37"
  ],
  "animations": true,
  "responsive": true
}
```

---

### Developer Agent

Converts the website plan into a project specification.

Example:

- Framework
- Bundler
- Styling
- Components
- Pages

---

### Architect Agent *(Upcoming)*

Determines the complete folder structure and required files before code generation begins.

---

### Code Generator *(Upcoming)*

Generates individual source files for the project.

Examples:

- App.jsx
- Navbar.jsx
- Footer.jsx
- package.json
- vite.config.js

---

### Validator *(Upcoming)*

Automatically checks the generated project for errors.

Responsibilities include:

- Build validation
- Missing imports
- Syntax checking
- AI-powered error correction

---

### Publisher *(Upcoming)*

Publishes generated projects directly to GitHub and deploys them using GitHub Pages.

---

# ⚙️ Technology Stack

## Backend

- Python
- FastAPI
- Pydantic
- Python Dotenv

## Artificial Intelligence

- Groq API
- Llama 3.3 70B
- Provider Abstraction Layer

## Frontend Generation

- React
- Vite
- Tailwind CSS

## Deployment

- GitHub API
- GitHub Pages

---

# 📂 Project Structure

```
Genesis/
│
├── backend/
│   │
│   ├── app/
│   │   ├── agents/
│   │   ├── github/
│   │   ├── llm/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   │
│   ├── .env
│   ├── requirements.txt
│   └── test_groq.py
│
├── frontend/
│
├── generated_projects/
│
├── README.md
├── LICENSE
└── .gitignore
```

---

# 🎯 Vision

Genesis aims to become an autonomous AI software engineer capable of:

- Understanding natural language requirements
- Planning complete web applications
- Designing project architecture
- Generating production-ready source code
- Validating generated projects
- Automatically fixing errors
- Publishing projects to GitHub
- Deploying websites to GitHub Pages
- Iteratively improving websites through conversation

---


# 🤝 Contributing

Genesis is currently an active development project.

Contributions, suggestions, and feature requests are welcome.

---

# 📄 License

This project is licensed under the MIT License.

---

## ⭐ About Genesis

Genesis is more than a website generator. It is being built as an AI software engineering platform that follows a structured development workflow—from understanding requirements to generating, validating, and deploying complete web applications.

The goal is to make software development more accessible by allowing users to create production-ready websites using natural language.
