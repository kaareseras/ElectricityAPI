from fastapi import HTTPException

from src.fastapi_app.config.config import get_settings
from src.fastapi_app.models.firmware import Firmware
from src.fastapi_app.responses.firmware import FirmwareResponse

settings = get_settings()


async def fetch_firmware_details(firmware_id, session):
    firmware = session.query(Firmware).filter(Firmware.id == firmware_id).first()
    _error = ""
    if not firmware:
        raise HTTPException(status_code=404, detail="Firmware not found.")

    my_firmware = FirmwareResponse(
        id=firmware.id,
        devicetype_id=firmware.devicetype_id,
        version=firmware.version,
        filename=firmware.filename,
        repo_url=firmware.repo_url,
        is_active=firmware.is_active,
        created_at=firmware.created_at,
        error=_error,
    )

    return my_firmware


async def fetch_firmwares(session):
    firmwares = session.query(Firmware).order_by(Firmware.created_at.desc()).all()

    my_firmwares = []
    for firmware in firmwares:
        my_firmware = FirmwareResponse(
            id=firmware.id,
            devicetype_id=firmware.devicetype_id,
            version=firmware.version,
            filename=firmware.filename,
            repo_url=firmware.repo_url,
            is_active=firmware.is_active,
            created_at=firmware.created_at,
        )
        my_firmwares.append(my_firmware)

    return my_firmwares


async def delete_firmware(pk, session):
    firmware = session.query(Firmware).filter(Firmware.id == pk).first()
    if not firmware:
        raise HTTPException(status_code=404, detail="Firmware not found.")
    session.delete(firmware)
    session.commit()
    return {"message": "Firmware deleted successfully."}


async def insert_firmware(data, session):
    existing_firmware = (
        session.query(Firmware)
        .filter(Firmware.version == data.version, Firmware.devicetype_id == data.devicetype_id)
        .first()
    )
    if existing_firmware:
        raise HTTPException(status_code=400, detail="Firmware with this version for the device type already exists.")

    new_firmware = Firmware(
        devicetype_id=data.devicetype_id,
        version=data.version,
        filename=data.filename,
        repo_url=data.repo_url,
        is_active=data.is_active,
        created_at=data.created_at,
    )
    session.add(new_firmware)
    session.commit()
    session.refresh(new_firmware)
    return await fetch_firmware_details(new_firmware.id, session)


async def update_firmware(firmware_id, data, session):
    firmware = session.query(Firmware).filter(Firmware.id == firmware_id).first()
    if not firmware:
        raise HTTPException(status_code=404, detail="Firmware not found.")

    firmware.devicetype_id = data.devicetype_id
    firmware.version = data.version
    firmware.filename = data.filename
    firmware.repo_url = data.repo_url
    firmware.is_active = data.is_active
    firmware.created_at = data.created_at

    session.commit()
    return await fetch_firmware_details(firmware.id, session)
