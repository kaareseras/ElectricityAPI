import logging
import os
import pathlib

from azure.monitor.opentelemetry import configure_azure_monitor
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from .config.database import get_db_session
from .models.models import Restaurant, Review

# Setup logger and Azure Monitor:
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    configure_azure_monitor()


def create_application():
    application = FastAPI()
    application.include_router(Restaurant.restaurant_router)

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
async def index(request: Request, session: Session = Depends(get_db_session)):
    logger.info("root called")

    statement = (
        select(Restaurant, func.avg(Review.rating).label("avg_rating"), func.count(Review.id).label("review_count"))
        .outerjoin(Review, Review.restaurant_id == Restaurant.id)
        .group_by(Restaurant.id)
    )
    results = session.execute(statement).all()

    restaurants = []
    for restaurant, avg_rating, review_count in results:
        restaurant_dict = {
            "id": restaurant.id,
            "name": restaurant.name,
            "street_address": restaurant.street_address,
            "description": restaurant.description,
        }
        restaurant_dict["avg_rating"] = avg_rating
        restaurant_dict["review_count"] = review_count
        restaurant_dict["stars_percent"] = round((float(avg_rating) / 5.0) * 100) if review_count > 0 else 0
        restaurants.append(restaurant_dict)

    return templates.TemplateResponse("index.html", {"request": request, "restaurants": restaurants})
