import logging
import os
import pathlib
import time

import python_multipart  # noqa
from azure.monitor.opentelemetry import configure_azure_monitor
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.fastapi_app.config.config import get_settings
from src.fastapi_app.routes import (
    admin,
    charge,
    chargeowner,
    copilot,
    device,
    devicetype,
    firmware,
    hardware,
    spotprice,
    tarif,
    tax,
    user,
    watermark,
)

# Track startup time
startup_start = time.time()

config = get_settings()

# Setup logger and Azure Monitor:
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

# Add console handler if not already present
if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    try:
        configure_azure_monitor()
        logger.info("Azure Monitor configured successfully")
    except Exception as e:
        logger.warning(f"Failed to configure Azure Monitor: {e}")
        # Don't fail startup if Azure Monitor setup fails


def create_application():
    logger.info("Starting FastAPI application creation...")

    application = FastAPI(
        title="Tax API",
        description="FastAPI Tax Management System",
        version="1.0.0",
        docs_url="/docs",  # Always enabled
        redoc_url="/redoc",  # Always enabled
    )

    # Include routers with error handling
    try:
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
        application.include_router(devicetype.devicetype_router)
        application.include_router(copilot.copilot_router)
        application.include_router(watermark.watermark_router)
        application.include_router(firmware.firmware_router)
        application.include_router(hardware.hardware_router)
        logger.info("All routers loaded successfully")
    except Exception as e:
        logger.error(f"Error loading routers: {e}")
        raise

    # Tillad CORS for Vue-app
    origins = [
        "https://thankful-glacier-0d5087003.6.azurestaticapps.net",  # Azure Static Web App
        "https://mcp-server.calmbay-a3cdc274.swedencentral.azurecontainerapps.io",  # MCP server
        "http://localhost:3000",  # Lokalt udviklingsmiljø
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Kun disse domæner må tilgå API'et
        allow_credentials=True,
        allow_methods=["*"],  # Tillad alle HTTP-metoder (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],  # Tillad alle headers
    )

    logger.info("FastAPI application created successfully")
    return application


# Setup FastAPI app:
app = create_application()
parent_path = pathlib.Path(__file__).parent.parent
app.mount("/mount", StaticFiles(directory=parent_path / "static"), name="static")
templates = Jinja2Templates(directory=parent_path / "templates")
templates.env.globals["prod"] = os.environ.get("RUNNING_IN_PRODUCTION", False)
# Use relative path for url_for, so that it works behind a proxy like Codespaces
templates.env.globals["url_for"] = app.url_path_for


# Add startup and shutdown events
@app.on_event("startup")
async def startup_event():
    startup_time = time.time() - startup_start
    logger.info(f"Application startup completed in {startup_time:.2f} seconds")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown initiated")
    # Ensure clean shutdown
    import asyncio

    await asyncio.sleep(0.1)  # Small delay to ensure clean shutdown
    logger.info("Application shutdown completed")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    logger.info("root called")
    return templates.TemplateResponse("index.html", {"request": request})
