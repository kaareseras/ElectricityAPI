from fastapi import HTTPException
from sqlalchemy import and_

from src.fastapi_app.config.config import get_settings
from src.fastapi_app.models.devicetype import DeviceType
from src.fastapi_app.responses.devicetype import DeviceTypeResponse

settings = get_settings()


async def fetch_devicetype_details(device_type_id, session):
    devicetype = session.query(DeviceType).filter(DeviceType.id == device_type_id).first()
    _error = ""
    if not devicetype:
        raise HTTPException(status_code=404, detail="DeviceType not found.")

    my_devicetype = DeviceTypeResponse(
        id=devicetype.id,
        name=devicetype.name,
        hw_version=devicetype.hw_version,
        sw_version=devicetype.sw_version,
        sw_date=devicetype.sw_date,
        error=_error,
    )

    return my_devicetype


async def fetch_devicetype_by_name(name, session):
    devicetype = session.query(DeviceType).filter(DeviceType.name == name).first()
    _error = ""
    if not devicetype:
        raise HTTPException(status_code=404, detail="DeviceType not found.")

    my_devicetype = DeviceTypeResponse(
        id=devicetype.id,
        name=devicetype.name,
        hw_version=devicetype.hw_version,
        sw_version=devicetype.sw_version,
        sw_date=devicetype.sw_date,
        error=_error,
    )

    return my_devicetype


async def fetch_devicetypes(session):
    devicetypes = session.query(DeviceType).order_by(DeviceType.name).all()
    _error = ""
    if not devicetypes:
        raise HTTPException(status_code=404, detail="DeviceTypes not found.")

    my_devicetypes = []
    for devicetype in devicetypes:
        my_devicetype = DeviceTypeResponse(
            id=devicetype.id,
            name=devicetype.name,
            hw_version=devicetype.hw_version,
            sw_version=devicetype.sw_version,
            sw_date=devicetype.sw_date,
            error=_error,
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


async def upsert_devicetype(data, session):
    new_devicetype = DeviceType()
    new_devicetype.name = data.name
    new_devicetype.hw_version = data.hw_version
    new_devicetype.sw_version = data.sw_version
    new_devicetype.sw_date = data.sw_date

    existing_devicetype = (
        session.query(DeviceType)
        .filter(
            and_(
                DeviceType.name == data.name,
                DeviceType.hw_version == data.hw_version,
                DeviceType.sw_version == data.sw_version,
            )
        )
        .first()
    )

    if not existing_devicetype:
        session.add(new_devicetype)
        session.commit()
        session.refresh(new_devicetype)
        return await fetch_devicetype_details(new_devicetype.id, session)
    else:
        # Optionally update fields if you want to allow updates
        existing_devicetype.sw_date = data.sw_date
        session.commit()
        return await fetch_devicetype_details(existing_devicetype.id, session)
