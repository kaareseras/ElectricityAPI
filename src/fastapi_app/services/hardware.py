from datetime import datetime, timezone

from fastapi import HTTPException

from src.fastapi_app.config.config import get_settings
from src.fastapi_app.models.hardware import Hardware
from src.fastapi_app.responses.hardware import HardwareResponse

settings = get_settings()


async def fetch_hardware_details(hardware_id, session):
    hardware = session.query(Hardware).filter(Hardware.id == hardware_id).first()
    _error = ""
    if not hardware:
        raise HTTPException(status_code=404, detail="Hardware not found.")

    my_hardware = HardwareResponse(
        id=hardware.id,
        devicetype_id=hardware.devicetype_id,
        version=hardware.version,
        name=hardware.name,
        description=hardware.description,
        is_active=hardware.is_active,
        created_at=hardware.created_at,
    )

    return my_hardware


async def fetch_hardware_by_devicetype(devicetype_id, session):
    hardwares = (
        session.query(Hardware)
        .filter(Hardware.devicetype_id == devicetype_id)
        .order_by(Hardware.created_at.desc())
        .all()
    )

    my_hardwares = []
    for hardware in hardwares:
        my_hardware = HardwareResponse(
            id=hardware.id,
            devicetype_id=hardware.devicetype_id,
            version=hardware.version,
            name=hardware.name,
            description=hardware.description,
            is_active=hardware.is_active,
            created_at=hardware.created_at,
        )
        my_hardwares.append(my_hardware)

    return my_hardwares


async def fetch_hardware(session):
    hardwares = session.query(Hardware).order_by(Hardware.created_at.desc()).all()

    my_hardwares = []
    for hardware in hardwares:
        my_hardware = HardwareResponse(
            id=hardware.id,
            devicetype_id=hardware.devicetype_id,
            version=hardware.version,
            name=hardware.name,
            description=hardware.description,
            is_active=hardware.is_active,
            created_at=hardware.created_at,
        )
        my_hardwares.append(my_hardware)

    return my_hardwares


async def delete_hardware(pk, session):
    hardware = session.query(Hardware).filter(Hardware.id == pk).first()
    if not hardware:
        raise HTTPException(status_code=404, detail="Hardware not found.")
    session.delete(hardware)
    session.commit()
    return {"message": "Hardware deleted successfully."}


async def insert_hardware(data, session):
    existing_hardware = (
        session.query(Hardware)
        .filter(Hardware.version == data.version, Hardware.devicetype_id == data.devicetype_id)
        .first()
    )
    if existing_hardware:
        raise HTTPException(status_code=400, detail="Hardware with this version for the device type already exists.")

    new_hardware = Hardware(
        devicetype_id=data.devicetype_id,
        version=data.version,
        name=data.name,
        description=data.description,
        is_active=data.is_active,
        created_at=datetime.now(timezone.utc),
    )
    session.add(new_hardware)
    session.commit()
    session.refresh(new_hardware)
    return await fetch_hardware_details(new_hardware.id, session)


async def update_hardware(hardware_id, data, session):
    hardware = session.query(Hardware).filter(Hardware.id == hardware_id).first()
    if not hardware:
        raise HTTPException(status_code=404, detail="Hardware not found.")

    hardware.devicetype_id = data.devicetype_id
    hardware.version = data.version
    hardware.name = data.name
    hardware.description = data.description
    hardware.is_active = data.is_active

    session.commit()
    return await fetch_hardware_details(hardware.id, session)
