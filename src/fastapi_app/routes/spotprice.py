from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.fastapi_app.config.database import get_db_session
from src.fastapi_app.config.security import get_current_user
from src.fastapi_app.responses.spotprice import SpotpriceResponse
from src.fastapi_app.schemas.spotprice import AddSpotpriceRequest, PriceRequest
from src.fastapi_app.services import spotprice

spotprice_router = APIRouter(
    prefix="/spotprice",
    tags=["Spotprice"],
    responses={404: {"description": "Not found"}},
)


@spotprice_router.get("", status_code=status.HTTP_200_OK, response_model=list[SpotpriceResponse])
async def get_spotprices(session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    return await spotprice.fetch_spotprices(session)


@spotprice_router.get(
    "/date/area",
    status_code=status.HTTP_200_OK,
    response_model=list[SpotpriceResponse],
    operation_id="get_spotprices_by_date_area",
)
async def get_spotprices_by_date_area(
    pricearea: str, qdate: datetime = None, session: Session = Depends(get_db_session)
):
    print(f"Fetching spotprices for {pricearea} on {qdate}")
    return await spotprice.fetch_spotprices_for_date(session, qdate, pricearea)


@spotprice_router.get("/{pk}", status_code=status.HTTP_200_OK, response_model=SpotpriceResponse)
async def get_spotprice_info(pk: int, session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    return await spotprice.fetch_spotprice_details(pk, session)


@spotprice_router.post("", status_code=status.HTTP_200_OK, response_model=SpotpriceResponse)
async def add_new_spotprice(
    data: AddSpotpriceRequest, session: Session = Depends(get_db_session), user=Depends(get_current_user)
):
    return await spotprice.add_spotprice(data, session)


@spotprice_router.post("/bulk", status_code=status.HTTP_200_OK, response_model=list[SpotpriceResponse])
async def add_spotprices(
    data: list[AddSpotpriceRequest], session: Session = Depends(get_db_session), user=Depends(get_current_user)
):
    return await spotprice.add_spotprices(data, session)


@spotprice_router.delete("/{pk}", status_code=status.HTTP_200_OK)
async def delete_spotprice(pk: int, session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    return await spotprice.delete_spotprice(pk, session)


@spotprice_router.post("/nordpool", status_code=status.HTTP_200_OK)
async def load_spot_prices_endpoint(
    data: PriceRequest, session: Session = Depends(get_db_session), user=Depends(get_current_user)
):
    inserted = await spotprice.load_spot_prices(data, session)
    return {"inserted": inserted}
