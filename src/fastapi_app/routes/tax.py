from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.fastapi_app.config.database import get_db_session
from src.fastapi_app.config.security import get_current_user
from src.fastapi_app.responses.tax import TaxResponse
from src.fastapi_app.schemas.tax import AddTaxRequest
from src.fastapi_app.services import tax

tax_router = APIRouter(
    prefix="/tax",
    tags=["Tax"],
    responses={404: {"description": "Not found"}},
)


@tax_router.get("/id/{pk}", status_code=status.HTTP_200_OK, response_model=TaxResponse)
async def get_tax_info_by_id(pk: int, session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    return await tax.fetch_tax_details(pk, session)


@tax_router.get("/date", status_code=status.HTTP_200_OK, response_model=TaxResponse)
async def get_tax_info_by_dat(
    qdate: datetime = None,
    session: Session = Depends(get_db_session),
    user=Depends(get_current_user),
):
    if qdate is None:
        qdate = datetime.now().astimezone().date()
    return await tax.fetch_tax_by_date(qdate, session)


@tax_router.get("", status_code=status.HTTP_200_OK, response_model=list[TaxResponse])
async def get_tax_info(session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    return await tax.fetch_taxes(session)


@tax_router.post("", status_code=status.HTTP_200_OK, response_model=TaxResponse)
async def add_new_tax(data: AddTaxRequest, session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    return await tax.upsert_tax(data, session)


@tax_router.delete("/{pk}", status_code=status.HTTP_200_OK)
async def delete_tax(pk: int, session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    return await tax.delete_tax(pk, session)
