import logging
from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.fastapi_app.config.database import get_db_session
from src.fastapi_app.config.security import get_current_admin, get_current_user
from src.fastapi_app.responses.dayprice import DaypriceResponse
from src.fastapi_app.responses.device import DeviceResponse
from src.fastapi_app.schemas.device import AdoptDeviceRequest, UpdateDeviceRequest
from src.fastapi_app.services import device

device_router = APIRouter(
    prefix="/device",
    tags=["Device"],
    responses={404: {"description": "Not found"}},
)


@device_router.get("/uuid/{uuid}", status_code=status.HTTP_200_OK, response_model=DeviceResponse)
async def get_device_info(uuid: str, session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    return await device.fetch_device_details(uuid, session, user)


@device_router.get("/dayprices", status_code=status.HTTP_200_OK, response_model=DaypriceResponse)
async def get_device_dayprice(
    uuid: str,
    qdate: datetime = datetime.now().astimezone().date(),
    session: Session = Depends(get_db_session),
    user=Depends(get_current_user),
):
    logging.info(f"Fetching dayprice for device {uuid} on {qdate}")
    return await device.fetch_device_dayprice(uuid, qdate, session, user)


@device_router.get("", status_code=status.HTTP_200_OK, response_model=list[DeviceResponse])
async def get_all_devices_for_user(session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    return await device.fetch_devices_for_user(session, user)


@device_router.get("/all", status_code=status.HTTP_200_OK, response_model=list[DeviceResponse])
async def get_all_devices(session: Session = Depends(get_db_session), admin=Depends(get_current_admin)):
    return await device.fetch_devices(session)


@device_router.post("/{uuid}", status_code=status.HTTP_200_OK, response_model=DeviceResponse)
async def add_new_device(uuid: str, session: Session = Depends(get_db_session), admin=Depends(get_current_admin)):
    return await device.add_device(uuid, session)


@device_router.post("/adopt/{uuid}", status_code=status.HTTP_200_OK, response_model=DeviceResponse)
async def adopt_device(
    uuid: str, data: AdoptDeviceRequest, session: Session = Depends(get_db_session), user=Depends(get_current_user)
):
    return await device.adopt_device(uuid, data, session, user)


@device_router.put("/{uuid}", status_code=status.HTTP_200_OK, response_model=DeviceResponse)
async def update_device(
    uuid: str, data: UpdateDeviceRequest, session: Session = Depends(get_db_session), user=Depends(get_current_user)
):
    return await device.update_device(uuid, data, session, user)


@device_router.delete("/{uuid}", status_code=status.HTTP_200_OK)
async def delete_device(uuid: str, session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    return await device.delete_device(uuid, session, user)
