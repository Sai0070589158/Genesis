from fastapi import FastAPI
from pydantic import BaseModel

from backend.app.agents.planner import Planner

app = FastAPI(
    title="Genesis API",
    version="1.0.0"
)


planner = Planner()


class WebsiteRequest(BaseModel):
    prompt: str


@app.get("/")
def home():
    return {
        "message": "Welcome to Genesis 🚀"
    }


@app.post("/generate")
def generate(request: WebsiteRequest):

    plan = planner.plan(request.prompt)

    return {
        "status": "success",
        "plan": plan.model_dump()
    }