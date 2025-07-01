from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.fastapi_app.config.database import get_db_session
from src.fastapi_app.config.security import get_current_user
from src.fastapi_app.responses.devicetype import DeviceTypeResponse
from src.fastapi_app.schemas.devicetype import AddDeviceTypeRequest
from src.fastapi_app.services import devicetype

device_type_router = APIRouter(
    prefix="/devicetype",
    tags=["DeviceType"],
    responses={404: {"description": "Not found"}},
)


@device_type_router.get("/id/{pk}", status_code=status.HTTP_200_OK, response_model=DeviceTypeResponse)
async def get_device_type_by_id(pk: int, session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    return await devicetype.fetch_device_type_details(pk, session)


@device_type_router.get(
    "", status_code=status.HTTP_200_OK, response_model=list[DeviceTypeResponse], operation_id="get_all_device_types"
)
async def get_device_types(session: Session = Depends(get_db_session)):
    return await devicetype.fetch_device_types(session)


@device_type_router.post("", status_code=status.HTTP_200_OK, response_model=DeviceTypeResponse)
async def add_new_device_type(
    data: AddDeviceTypeRequest, session: Session = Depends(get_db_session), user=Depends(get_current_user)
):
    return await devicetype.upsert_device_type(data, session)


@device_type_router.delete("/{pk}", status_code=status.HTTP_200_OK)
async def delete_device_type(pk: int, session: Session = Depends(get_db_session), user=Depends(get_current_user)):
    return await devicetype.delete_device_type(pk, session)
