from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.fastapi_app.config.database import get_db_session
from src.fastapi_app.config.security import get_current_user
from src.fastapi_app.responses.chargeowner import ChargeownerListResponse, ChargeownerResponse
from src.fastapi_app.schemas.chargeowner import AddChargeownerRequest, UpdateChargeownerRequest
from src.fastapi_app.services import chargeowner

chargeowner_router = APIRouter(
    prefix="/chargeowner",
    tags=["Chargeowner"],
    responses={404: {"description": "Not found"}},
)


@chargeowner_router.get("", status_code=status.HTTP_200_OK, response_model=list[ChargeownerListResponse])
async def get_chargeowners(session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    return await chargeowner.fetch_chargeowners(session)


@chargeowner_router.get("/{pk}", status_code=status.HTTP_200_OK, response_model=ChargeownerResponse)
async def get_chargeowner_info(pk, session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    return await chargeowner.fetch_chargeowner_details(pk, session)


@chargeowner_router.post("", status_code=status.HTTP_200_OK, response_model=ChargeownerResponse)
async def add_new_chargeowner(
    data: AddChargeownerRequest, session: Session = Depends(get_db_session), user=Depends(get_current_user)
):
    return await chargeowner.add_chargeowner(data, session)


@chargeowner_router.put("/{pk}", status_code=status.HTTP_200_OK, response_model=ChargeownerResponse)
async def update_chargeowner(
    pk: int,
    data: UpdateChargeownerRequest,
    session: Session = Depends(get_db_session),
    user=Depends(get_current_user),
):
    return await chargeowner.update_chargeowner(data, session)


@chargeowner_router.delete("/{pk}", status_code=status.HTTP_200_OK)
async def delete_chargeowner(pk: int, session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    return await chargeowner.delete_chargeowner(pk, session)
