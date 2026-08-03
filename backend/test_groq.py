from backend.app.agents.developer import Developer
from backend.app.models.website_plan import WebsitePlan

plan = WebsitePlan(
    website_type="Luxury Hotel",
    pages=[
        "Home",
        "Rooms",
        "Booking",
        "Contact"
    ],
    theme="Luxury",
    color_scheme=[
        "#111827",
        "#D4AF37"
    ],
    animations=True,
    responsive=True
)

developer = Developer()

project = developer.generate_project(plan)

print(project.model_dump_json(indent=2))