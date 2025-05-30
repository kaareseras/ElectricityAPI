from datetime import datetime, timezone

from fastapi import HTTPException

from src.fastapi_app.config.config import get_settings
from src.fastapi_app.models.chargeowner import Chargeowner
from src.fastapi_app.responses.chargeowner import ChargeownerListResponse, ChargeownerResponse

settings = get_settings()


async def fetch_chargeowner_details(data, session):
    chargeowner = session.query(Chargeowner).filter(Chargeowner.id == data).first()
    _error = ""
    if not chargeowner:
        raise HTTPException(status_code=404, detail="Chargeowner not found.")

    my_chargeowner = ChargeownerResponse(
        id=chargeowner.id,
        glnnumber=chargeowner.glnnumber,
        compagny=chargeowner.compagny,
        chargetype=chargeowner.chargetype,
        chargetypecode=chargeowner.chargetypecode,
        is_active=chargeowner.is_active,
        created_at=chargeowner.created_at,
        updated_at=chargeowner.updated_at,
        error=_error,
    )

    return my_chargeowner


async def delete_chargeowner(data, session):
    chargeowner = session.query(Chargeowner).filter(Chargeowner.id == data).first()
    if not chargeowner:
        raise HTTPException(status_code=404, detail="Chargeowner not found.")
    session.delete(chargeowner)
    session.commit()
    return {"message": "Chargeowner deleted successfully."}


async def update_chargeowner(data, session):
    chargeowner = session.query(Chargeowner).filter(Chargeowner.id == data.id).first()

    if not chargeowner:
        raise HTTPException(status_code=404, detail="Chargeowner not found.")

    chargeowner.glnnumber = data.glnnumber
    chargeowner.compagny = data.compagny
    chargeowner.chargetype = data.chargetype
    chargeowner.chargetypecode = data.chargetypecode
    chargeowner.is_active = data.is_active
    chargeowner.updated_at = datetime.now(timezone.utc)
    session.commit()
    session.refresh(chargeowner)

    return await fetch_chargeowner_details(chargeowner.id, session)


async def add_chargeowner(data, session):
    chargeowner = Chargeowner()
    chargeowner.glnnumber = data.glnnumber
    chargeowner.compagny = data.compagny
    chargeowner.chargetype = data.chargetype
    chargeowner.chargetypecode = data.chargetypecode
    chargeowner.is_active = True
    chargeowner.created_at = datetime.now(timezone.utc)
    chargeowner.updated_at = datetime.now(timezone.utc)
    session.add(chargeowner)
    session.commit()
    session.refresh(chargeowner)

    return await fetch_chargeowner_details(chargeowner.id, session)


async def fetch_chargeowners(session):
    chargeowners = session.query(Chargeowner).all()

    my_chargeowners = []

    if not chargeowners:
        return []

    for chargeowner in chargeowners:
        my_chargeowners.append(
            ChargeownerListResponse(
                id=chargeowner.id,
                compagny=chargeowner.compagny,
                glnnumber=chargeowner.glnnumber,
                chargetype=chargeowner.chargetype,
                chargetypecode=chargeowner.chargetypecode,
                is_active=chargeowner.is_active,
                created_at=chargeowner.created_at,
                updated_at=chargeowner.updated_at,
            )
        )
    return my_chargeowners
