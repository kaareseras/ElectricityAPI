from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.fastapi_app.config.database import get_db_session
from src.fastapi_app.config.security import get_current_admin, get_current_user
from src.fastapi_app.responses.devicetype import DeviceTypeResponse
from src.fastapi_app.schemas.devicetype import DeviceTypeSchema
from src.fastapi_app.services import devicetype

devicetype_router = APIRouter(
    prefix="/devicetype",
    tags=["DeviceType"],
    responses={404: {"description": "Not found"}},
)


@devicetype_router.get("/id/{pk}", status_code=status.HTTP_200_OK, response_model=DeviceTypeResponse)
async def get_device_type_by_id(pk: int, session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    return await devicetype.fetch_devicetype_details(pk, session)


@devicetype_router.get(
    "", status_code=status.HTTP_200_OK, response_model=list[DeviceTypeResponse], operation_id="get_all_device_types"
)
async def get_devicetypes(session: Session = Depends(get_db_session)):
    return await devicetype.fetch_devicetypes(session)


@devicetype_router.post("", status_code=status.HTTP_201_CREATED, response_model=DeviceTypeResponse)
async def create_devicetype(
    data: DeviceTypeSchema, session: Session = Depends(get_db_session), user=Depends(get_current_admin)
):
    return await devicetype.insert_devicetype(data, session)


@devicetype_router.put("/{pk}", status_code=status.HTTP_200_OK, response_model=DeviceTypeResponse)
async def update_devicetype(
    pk: int, data: DeviceTypeSchema, session: Session = Depends(get_db_session), user=Depends(get_current_admin)
):
    return await devicetype.update_devicetype(pk, data, session)


@devicetype_router.delete("/{pk}", status_code=status.HTTP_200_OK)
async def delete_devicetype(pk: int, session: Session = Depends(get_db_session), user=Depends(get_current_admin)):
    return await devicetype.delete_devicetype(pk, session)
