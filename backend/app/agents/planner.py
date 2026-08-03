from pydantic import BaseModel


class WebsitePlan(BaseModel):
    website_type: str
    pages: list[str]
    theme: str
    color_scheme: list[str]
    animations: bool
    responsive: bool


class Planner:

    def plan(self, prompt: str) -> WebsitePlan:
        """
        Temporary planner.
        Later this will use an LLM.
        """

        return WebsitePlan(
            website_type="Portfolio",
            pages=[
                "Home",
                "About",
                "Projects",
                "Contact"
            ],
            theme="Modern",
            color_scheme=[
                "#2563EB",
                "#F8FAFC"
            ],
            animations=True,
            responsive=True
        )