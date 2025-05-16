from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.fastapi_app.config.database import get_db_session
from src.fastapi_app.config.security import get_current_user
from src.fastapi_app.responses.tarif import TarifResponse
from src.fastapi_app.schemas.tarif import AddTarifRequest
from src.fastapi_app.services import tarif

tarif_router = APIRouter(
    prefix="/tarif",
    tags=["Tarif"],
    responses={404: {"description": "Not found"}},
)


@tarif_router.get("/id/{pk}", status_code=status.HTTP_200_OK, response_model=TarifResponse)
async def get_tarif_info(pk: int, session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    return await tarif.fetch_tarif_details(pk, session)


@tarif_router.get("/date", status_code=status.HTTP_200_OK, response_model=TarifResponse)
async def get_tarif_info(
    qdate: datetime = datetime.now().astimezone().date(),
    session: Session = Depends(get_db_session),
    user=Depends(get_current_user),
):
    return await tarif.fetch_tarif_by_date(qdate, session)


@tarif_router.get("", status_code=status.HTTP_200_OK, response_model=list[TarifResponse])
async def get_tarif_info(session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    return await tarif.fetch_tarifs(session)


@tarif_router.post("", status_code=status.HTTP_200_OK, response_model=TarifResponse)
async def add_new_tarif(
    data: AddTarifRequest, session: Session = Depends(get_db_session), user=Depends(get_current_user)
):
    return await tarif.add_tarif(data, session)


@tarif_router.delete("/{pk}", status_code=status.HTTP_200_OK)
async def delete_tarif(pk: int, session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    return await tarif.delete_tarif(pk, session)
