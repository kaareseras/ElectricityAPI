import logging
import os
import pathlib

from azure.monitor.opentelemetry import configure_azure_monitor
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.fastapi_app.routes import admin, restaurant, user

# Setup logger and Azure Monitor:
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    configure_azure_monitor()


def create_application():
    application = FastAPI()
    application.include_router(restaurant.restaurant_router)
    application.include_router(user.user_router)
    application.include_router(user.guest_router)
    application.include_router(user.auth_router)
    application.include_router(admin.admin_router)

    # Tillad CORS for frontend (localhost:3000)
    origins = [
        "http://localhost:3000",  # Tillad anmodninger fra Vue-app på port 3000
        # Du kan også tilføje flere domæner her, f.eks.:
        # "http://localhost:8080",  # Hvis du har andre lokale apps
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Kun disse domæner må tilgå API'et
        allow_credentials=True,
        allow_methods=["*"],  # Tillad alle HTTP-metoder (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],  # Tillad alle headers
    )

    return application


# Setup FastAPI app:
app = create_application()
parent_path = pathlib.Path(__file__).parent.parent
app.mount("/mount", StaticFiles(directory=parent_path / "static"), name="static")
templates = Jinja2Templates(directory=parent_path / "templates")
templates.env.globals["prod"] = os.environ.get("RUNNING_IN_PRODUCTION", False)
# Use relative path for url_for, so that it works behind a proxy like Codespaces
templates.env.globals["url_for"] = app.url_path_for


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    logger.info("root called")
    return templates.TemplateResponse("index.html", {"request": request})
