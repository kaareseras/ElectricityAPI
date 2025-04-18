import logging
from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.fastapi_app.config.database import get_db_session
from src.fastapi_app.models.models import Restaurant, Review

templates = Jinja2Templates(directory="src/fastapi_app/templates")

# Configure logger
logger = logging.getLogger("restaurant_logger")
logger.setLevel(logging.INFO)

templates = Jinja2Templates(directory="src/fastapi_app/templates")


restaurant_router = APIRouter(
    prefix="/restaurant",
    tags=["Restaurant"],
    responses={404: {"description": "Not found"}},
)

restaurant_router.get("/create", response_class=HTMLResponse)


async def create_restaurant(request: Request):
    logger.info("Request for add restaurant page received")
    return templates.TemplateResponse("create_restaurant.html", {"request": request})


restaurant_router.post("/add", response_class=RedirectResponse)


async def add_restaurant(
    request: Request,
    restaurant_name: str = Form(...),
    street_address: str = Form(...),
    description: str = Form(...),
    session: Session = Depends(get_db_session),
):
    logger.info("name: %s address: %s description: %s", restaurant_name, street_address, description)
    restaurant = Restaurant()
    restaurant.name = restaurant_name
    restaurant.street_address = street_address
    restaurant.description = description
    session.add(restaurant)
    session.commit()
    session.refresh(restaurant)

    return RedirectResponse(url=f"/details/{restaurant.id}", status_code=status.HTTP_303_SEE_OTHER)


restaurant_router.get("/details/{id}", response_class=HTMLResponse)


async def details(request: Request, id: int, session: Session = Depends(get_db_session)):
    restaurant = session.query(Restaurant).filter(Restaurant.id == id).first()
    reviews = session.query(Review).join(Review.restaurant).filter(Review.restaurant_id == id).all()

    review_count = len(reviews)

    avg_rating = 0
    if review_count > 0:
        avg_rating = sum(review.rating for review in reviews if review.rating is not None) / review_count

    restaurant_dict = {
        "id": restaurant.id,
        "name": restaurant.name,
        "street_address": restaurant.street_address,
        "description": restaurant.description,
    }
    restaurant_dict["avg_rating"] = avg_rating
    restaurant_dict["review_count"] = review_count
    restaurant_dict["stars_percent"] = round((float(avg_rating) / 5.0) * 100) if review_count > 0 else 0

    return templates.TemplateResponse(
        "details.html", {"request": request, "restaurant": restaurant_dict, "reviews": reviews}
    )


restaurant_router.post("/review/{id}", response_class=RedirectResponse)


async def add_review(
    request: Request,
    id: int,
    user_name: str = Form(...),
    rating: str = Form(...),
    review_text: str = Form(...),
    session: Session = Depends(get_db_session),
):
    review = Review()
    review.restaurant_id = id
    review.review_date = datetime.now()
    review.user_name = user_name
    review.rating = int(rating)
    review.review_text = review_text
    session.add(review)
    session.commit()

    return RedirectResponse(url=f"/details/{id}", status_code=status.HTTP_303_SEE_OTHER)
