import ast
import logging
from datetime import datetime, timezone

from fastapi import HTTPException

from src.fastapi_app.config.config import get_settings
from src.fastapi_app.models.charge import Charge
from src.fastapi_app.models.chargeowner import Chargeowner
from src.fastapi_app.responses.chargeowner import ChargeownerLatestCharge, ChargeownerListResponse, ChargeownerResponse

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

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


"""This function fetches the latest charge for each chargeowner.
It uses a subquery to find the latest charge based on the maximum valid_to date for each chargeowner.
The subquery is then outer joined with the Chargeowner table to get the required details.
The results are returned as a list of ChargeownerLatestCharge objects."""


async def fetch_chargeowner_with_latest_charge(session):
    chargeowners = session.query(Chargeowner).all()

    chargeownerLatestCharge: list[ChargeownerLatestCharge] = []

    for chargeowner in chargeowners:
        typecodes = ast.literal_eval(chargeowner.chargetypecode)

        for code in typecodes:
            logger.info(f"Processing chargeowner: {chargeowner.id}, typecode: {code}")

            # Query the latest charge for this chargeowner and typecode
            _charge = (
                session.query(Charge)
                .filter(Charge.chargeowner_id == chargeowner.id)
                .order_by(Charge.valid_to.desc())
                .limit(1)
                .one_or_none()
            )

            latestCharge = ChargeownerLatestCharge(
                compagny=chargeowner.compagny,
                chargetype=chargeowner.chargetype,
                chargetypecode=code,
                glnnumber=chargeowner.glnnumber,
                valid_from=_charge.valid_from if _charge else None,
                valid_to=_charge.valid_to if _charge else None,
            )

            chargeownerLatestCharge.append(latestCharge)

    return chargeownerLatestCharge
