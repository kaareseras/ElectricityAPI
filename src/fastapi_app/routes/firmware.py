from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.fastapi_app.config.database import get_db_session
from src.fastapi_app.config.security import get_current_admin
from src.fastapi_app.responses.firmware import FirmwareResponse
from src.fastapi_app.schemas.firmware import FirmwareSchema
from src.fastapi_app.services import firmware

firmware_router = APIRouter(
    prefix="/firmware",
    tags=["Firmware"],
    responses={404: {"description": "Not found"}},
)


@firmware_router.get("/{pk}", status_code=status.HTTP_200_OK, response_model=FirmwareResponse)
async def get_firmware_by_id(pk: int, session: Session = Depends(get_db_session), user=Depends(get_current_admin)):
    return await firmware.fetch_firmware_details(pk, session)


@firmware_router.get("/by-devicetype/{pk}", status_code=status.HTTP_200_OK, response_model=List[FirmwareResponse])
async def get_firmware_by_devicetype(
    pk: int, session: Session = Depends(get_db_session), user=Depends(get_current_admin)
):
    return await firmware.fetch_firmware_by_devicetype(pk, session)


@firmware_router.get("", status_code=status.HTTP_200_OK, response_model=list[FirmwareResponse])
async def get_firmwares(session: Session = Depends(get_db_session), user=Depends(get_current_admin)):
    return await firmware.fetch_firmwares(session)


@firmware_router.post("", status_code=status.HTTP_201_CREATED, response_model=FirmwareResponse)
async def create_firmware(
    data: FirmwareSchema, session: Session = Depends(get_db_session), user=Depends(get_current_admin)
):
    return await firmware.insert_firmware(data, session)


@firmware_router.put("/{pk}", status_code=status.HTTP_200_OK, response_model=FirmwareResponse)
async def update_firmware(
    pk: int, data: FirmwareSchema, session: Session = Depends(get_db_session), user=Depends(get_current_admin)
):
    return await firmware.update_firmware(pk, data, session)


@firmware_router.delete("/{pk}", status_code=status.HTTP_200_OK)
async def delete_firmware(pk: int, session: Session = Depends(get_db_session), user=Depends(get_current_admin)):
    return await firmware.delete_firmware(pk, session)
