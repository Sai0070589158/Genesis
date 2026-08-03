from pydantic import BaseModel


class WebsitePlan(BaseModel):
    website_type: str
    pages: list[str]
    theme: str
    color_scheme: list[str]
    animations: bool
    responsive: bool