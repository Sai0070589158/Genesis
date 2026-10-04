import os
import time

from dotenv import load_dotenv
from groq import Groq

from backend.app.llm.provider import LLMProvider


load_dotenv("backend/.env")


class GroqProvider(LLMProvider):

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

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

                return content
            except Exception as error:

                error_text = str(error)
                error_lower = error_text.lower()

                # Daily token quota cannot be fixed bypy -m backend.test_full_generation
                # short retries. Fail immediately.
                if (
                    "tokens per day" in error_lower
                    or "tpd" in error_lower
                ):
                    raise RuntimeError(
                        "Groq daily token limit reached. "
                        "Please wait for the quota to reset "
                        "before generating another project."
                    ) from error

                # Temporary rate limits can be retried.
                if (
                    "429" in error_text
                    or "rate_limit" in error_lower
                    or "tokens per minute" in error_lower
                ):

                    if attempt == self.max_retries:
                        raise

                    wait_time = attempt * 4

                    print(
                        f"\nGroq temporary rate limit reached."
                        f" Waiting {wait_time}s "
                        f"before retry "
                        f"{attempt + 1}/"
                        f"{self.max_retries}..."
                    )

                    time.sleep(wait_time)

                else:
                    raise