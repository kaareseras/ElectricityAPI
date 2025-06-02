import logging
import os
import pathlib

import python_multipart  # noqa
from azure.monitor.opentelemetry import configure_azure_monitor
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_mcp import FastApiMCP

from src.fastapi_app.config.config import get_settings
from src.fastapi_app.routes import admin, charge, chargeowner, copilot, device, spotprice, tarif, tax, user

config = get_settings()

# Setup logger and Azure Monitor:
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    configure_azure_monitor()


def create_application():
    application = FastAPI()
    application.include_router(user.user_router)
    application.include_router(user.guest_router)
    application.include_router(user.auth_router)
    application.include_router(admin.admin_router)
    application.include_router(chargeowner.chargeowner_router)
    application.include_router(charge.charge_router)
    application.include_router(spotprice.spotprice_router)
    application.include_router(tax.tax_router)
    application.include_router(tarif.tarif_router)
    application.include_router(device.device_router)
    application.include_router(copilot.copilot_router)

    # Tillad CORS for Vue-app
    origins = [
        "https://thankful-glacier-0d5087003.6.azurestaticapps.net",  # Azure Static Web App
        "http://localhost:3000",  # Lokalt udviklingsmiljø
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Kun disse domæner må tilgå API'et
        allow_credentials=True,
        allow_methods=["*"],  # Tillad alle HTTP-metoder (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],  # Tillad alle headers
    )
    application.add_middleware(HTTPSRedirectMiddleware)

    return application


# Setup FastAPI app:
app = create_application()
parent_path = pathlib.Path(__file__).parent.parent
app.mount("/mount", StaticFiles(directory=parent_path / "static"), name="static")
templates = Jinja2Templates(directory=parent_path / "templates")
templates.env.globals["prod"] = os.environ.get("RUNNING_IN_PRODUCTION", False)
# Use relative path for url_for, so that it works behind a proxy like Codespaces
templates.env.globals["url_for"] = app.url_path_for


# Filter by including specific operation IDs
include_operations_mcp = FastApiMCP(
    app,
    name="Tax API MCP - Included Operations",
    include_operations=["get_all_taxes", "get_spotprices_by_date_area"],
)

include_operations_mcp.mount(mount_path="/" + config.MCP_ROUTE)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    logger.info("root called")
    return templates.TemplateResponse("index.html", {"request": request})
