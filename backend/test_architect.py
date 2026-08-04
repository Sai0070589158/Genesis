from backend.app.agents.architect import Architect
from backend.app.models.project_spec import ProjectSpec

spec = ProjectSpec(
    framework="React",
    bundler="Vite",
    styling="Tailwind CSS",
    pages=[
        "Home",
        "Rooms",
        "Booking",
        "Contact"
    ],
    components=[
        "Header",
        "Footer",
        "RoomCard",
        "BookingForm"
    ]
)

architect = Architect()

blueprint = architect.design(spec)

print(blueprint.model_dump_json(indent=2))