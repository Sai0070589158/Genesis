import os
import time

from dotenv import load_dotenv
from groq import Groq

from backend.app.llm.provider import LLMProvider


load_dotenv("backend/.env")


class GroqProvider(LLMProvider):

    def __init__(self):

        api_key = os.getenv(
            "GROQ_API_KEY"
        )

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found in .env"
            )

        self.client = Groq(
            api_key=api_key
        )

        self.model = "openai/gpt-oss-120b"

        self.max_retries = 3

    def generate(
        self,
        prompt: str
    ) -> str:

        for attempt in range(
            1,
            self.max_retries + 1
        ):

            try:

                response = (
                    self.client
                    .chat
                    .completions
                    .create(
                        model=self.model,
                        temperature=0.3,
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )
                )

                return (
                    response
                    .choices[0]
                    .message
                    .content
                )

            except Exception as error:

                error_text = str(error)

                # Retry rate-limit errors.
                if (
                    "429" in error_text
                    or "rate_limit" in error_text.lower()
                    or "tokens per minute" in error_text.lower()
                ):

                    if attempt == self.max_retries:
                        raise

                    wait_time = attempt * 4

                    print(
                        f"\nGroq rate limit reached."
                        f" Waiting {wait_time}s "
                        f"before retry "
                        f"{attempt + 1}/"
                        f"{self.max_retries}..."
                    )

                    time.sleep(
                        wait_time
                    )

                else:
                    raise