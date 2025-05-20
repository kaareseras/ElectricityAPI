from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.fastapi_app.config.database import get_db_session
from src.fastapi_app.config.security import get_current_user
from src.fastapi_app.responses.charge import ChargeResponse
from src.fastapi_app.schemas.charge import AddChargeRequest
from src.fastapi_app.services import charge

charge_router = APIRouter(
    prefix="/charge",
    tags=["Charge"],
    responses={404: {"description": "Not found"}},
)


@charge_router.get("/{pk}", status_code=status.HTTP_200_OK, response_model=ChargeResponse)
async def get_charge_info(pk: int, session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    return await charge.fetch_charge_details(pk, session)


@charge_router.get("/gln/{chargeowner_glnnumber}", status_code=status.HTTP_200_OK, response_model=list[ChargeResponse])
async def get_charger_info(
    chargeowner_glnnumber: str, session: Session = Depends(get_db_session), user=Depends(get_current_user)
):
    return await charge.fetch_charges_for_chargeowner(session, chargeowner_glnnumber)


@charge_router.get("/date/gln", status_code=status.HTTP_200_OK, response_model=ChargeResponse)
async def get_charges(
    chargeowner_glnnumber: str,
    qdate: datetime = None,
    session: Session = Depends(get_db_session),
    user=Depends(get_current_user),
):
    if qdate is None:
        qdate = datetime.now().astimezone().date()

    return await charge.fetch_charges_for_date_and_gln(session, qdate, chargeowner_glnnumber)


@charge_router.post("", status_code=status.HTTP_200_OK, response_model=ChargeResponse)
async def add_new_charge(
    data: AddChargeRequest, session: Session = Depends(get_db_session), user=Depends(get_current_user)
):
    return await charge.add_charge(data, session)


@charge_router.delete("/{pk}", status_code=status.HTTP_200_OK)
async def delete_charge(pk: int, session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    return await charge.delete_charge(pk, session)
