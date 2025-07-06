from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.fastapi_app.config.database import get_db_session
from src.fastapi_app.config.security import get_current_admin, get_current_user
from src.fastapi_app.responses.hardware import HardwareResponse
from src.fastapi_app.schemas.hardware import HardwareSchema
from src.fastapi_app.services import hardware

hardware_router = APIRouter(
    prefix="/hardware",
    tags=["Hardware"],
    responses={404: {"description": "Not found"}},
)


@hardware_router.get("/{pk}", status_code=status.HTTP_200_OK, response_model=HardwareResponse)
async def get_hardware_by_id(pk: int, session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    return await hardware.fetch_hardware_details(pk, session)


@hardware_router.get("/by-devicetype/{pk}", status_code=status.HTTP_200_OK, response_model=List[HardwareResponse])
async def get_hardware_by_devicetype(
    pk: int, session: Session = Depends(get_db_session), user=Depends(get_current_admin)
):
    return await hardware.fetch_hardware_by_devicetype(pk, session)


@hardware_router.get(
    "", status_code=status.HTTP_200_OK, response_model=list[HardwareResponse], operation_id="get_all_hardware"
)
async def get_hardware(session: Session = Depends(get_db_session)):
    return await hardware.fetch_hardware(session)


@hardware_router.post("", status_code=status.HTTP_201_CREATED, response_model=HardwareResponse)
async def create_hardware(
    data: HardwareSchema, session: Session = Depends(get_db_session), user=Depends(get_current_admin)
):
    return await hardware.insert_hardware(data, session)


@hardware_router.put("/{pk}", status_code=status.HTTP_200_OK, response_model=HardwareResponse)
async def update_hardware(
    pk: int, data: HardwareSchema, session: Session = Depends(get_db_session), user=Depends(get_current_admin)
):
    return await hardware.update_hardware(pk, data, session)


@hardware_router.delete("/{pk}", status_code=status.HTTP_200_OK)
async def delete_hardware(pk: int, session: Session = Depends(get_db_session), user=Depends(get_current_admin)):
    return await hardware.delete_hardware(pk, session)
