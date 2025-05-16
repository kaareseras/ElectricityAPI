from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.fastapi_app.config.database import get_db_session
from src.fastapi_app.responses.dayprice import DaypriceResponse
from src.fastapi_app.services import device

device_router = APIRouter(
    prefix="/dayprice",
    tags=["Dayprice"],
    responses={404: {"description": "Not found"}},
)


@device_router.get("/{uuid}", status_code=status.HTTP_200_OK, response_model=DaypriceResponse)
async def get_device_info(
    uuid: str,
    session: Session = Depends(get_db_session),
    qdate: datetime = datetime.now().date,
):
    return await device.fetch_device_dayprice(uuid, qdate, session)
