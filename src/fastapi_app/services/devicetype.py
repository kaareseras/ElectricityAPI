from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager

from src.fastapi_app.config.config import get_settings
from src.fastapi_app.models.devicetype import DeviceType
from src.fastapi_app.models.firmware import Firmware
from src.fastapi_app.models.hardware import Hardware
from src.fastapi_app.responses.devicetype import DeviceTypeListResponse, DeviceTypeResponse

settings = get_settings()


async def fetch_devicetype_details(device_type_id, session):
    devicetype = session.query(DeviceType).filter(DeviceType.id == device_type_id).first()
    _error = ""
    if not devicetype:
        raise HTTPException(status_code=404, detail="DeviceType not found.")

    my_devicetype = DeviceTypeResponse(
        id=devicetype.id,
        name=devicetype.name,
        description=devicetype.description,
    )

    return my_devicetype


async def fetch_devicetypes_with_active_firmware_and_hardware(session):
    devicetypes = (
        session.query(DeviceType)
        .outerjoin(Firmware, and_(Firmware.devicetype_id == DeviceType.id, Firmware.is_active))
        .outerjoin(Hardware, and_(Hardware.devicetype_id == DeviceType.id, Hardware.is_active))
        .options(
            contains_eager(DeviceType.firmwares),
            contains_eager(DeviceType.hardwares),
        )
        .order_by(DeviceType.name)
        .all()
    )

    my_devicetypes = []

    for devicetype in devicetypes:
        firmware = devicetype.firmwares[0] if devicetype.firmwares else None
        hardware = devicetype.hardwares[0] if devicetype.hardwares else None

        my_devicetype = DeviceTypeListResponse(
            id=devicetype.id,
            name=devicetype.name,
            description=devicetype.description,
            created_at=devicetype.created_at,
            fw_version=firmware.version if firmware else None,
            fw_date=firmware.created_at if firmware else None,  # eller .release_date hvis det felt findes
            hw_version=hardware.version if hardware else None,
        )
        my_devicetypes.append(my_devicetype)

    return my_devicetypes


async def fetch_devicetypes(session):
    devicetypes = session.query(DeviceType).order_by(DeviceType.name).all()

    my_devicetypes = []
    for devicetype in devicetypes:
        my_devicetype = DeviceTypeResponse(
            id=devicetype.id,
            name=devicetype.name,
            description=devicetype.description,
        )
        my_devicetypes.append(my_devicetype)

    return my_devicetypes


async def delete_devicetype(pk, session):
    devicetype = session.query(DeviceType).filter(DeviceType.id == pk).first()
    if not devicetype:
        raise HTTPException(status_code=404, detail="DeviceType not found.")
    session.delete(devicetype)
    session.commit()
    return {"message": "DeviceType deleted successfully."}


async def insert_devicetype(data, session):
    existing_devicetype = session.query(DeviceType).filter(DeviceType.name == data.name).first()
    if existing_devicetype:
        raise HTTPException(status_code=400, detail="DeviceType with this name already exists.")

    new_devicetype = DeviceType(name=data.name, description=data.description, created_at=datetime.now(timezone.utc))
    session.add(new_devicetype)
    session.commit()
    session.refresh(new_devicetype)
    return await fetch_devicetype_details(new_devicetype.id, session)


async def update_devicetype(device_type_id, data, session):
    devicetype = session.query(DeviceType).filter(DeviceType.id == device_type_id).first()
    if not devicetype:
        raise HTTPException(status_code=404, detail="DeviceType not found.")

    devicetype.name = data.name
    devicetype.description = data.description

    session.commit()
    return await fetch_devicetype_details(devicetype.id, session)
