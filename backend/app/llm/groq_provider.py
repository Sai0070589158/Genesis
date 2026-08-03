import os

from dotenv import load_dotenv
from groq import Groq

from backend.app.llm.provider import LLMProvider

load_dotenv("backend/.env")


class GroqProvider(LLMProvider):

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env")

        self.client = Groq(api_key=api_key)

    def generate(self, prompt: str) -> str:

        system_prompt = """
You are an expert software architect.

Analyze the user's request and return ONLY valid JSON.

The JSON must have this exact format:

{
    "website_type": "",
    "pages": [],
    "theme": "",
    "color_scheme": [],
    "animations": true,
    "responsive": true
}

Return ONLY JSON.
Do not use markdown.
Do not explain anything.
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content