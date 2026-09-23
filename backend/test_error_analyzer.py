from backend.app.services.error_analyzer import ErrorAnalyzer


build_result = {
    "success": False,
    "stage": "npm run build",
    "output": "",
    "error": """
failed to load config from
C:\\Users\\saina\\Genesis\\generated_projects\\genesis_portfolio\\vite.config.js

Error: Cannot find module '@vitejs/plugin-react'
"""
}


analyzer = ErrorAnalyzer()

result = analyzer.analyze(build_result)

print("\n=== ERROR ANALYSIS ===")
print(result)