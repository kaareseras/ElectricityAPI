from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import and_, or_

from src.fastapi_app.config.config import get_settings
from src.fastapi_app.models.charge import Charge
from src.fastapi_app.models.chargeowner import Chargeowner
from src.fastapi_app.responses.charge import ChargeResponse

settings = get_settings()


async def fetch_charge_details(data, session):
    charge = session.query(Charge).filter(Charge.id == data).first()
    _error = ""
    if not charge:
        raise HTTPException(status_code=404, detail="Charge not found.")

    my_charge = ChargeResponse(
        id=charge.id,
        chargeowner_id=charge.chargeowner_id,
        charge_type=charge.charge_type,
        charge_type_code=charge.charge_type_code,
        note=charge.note,
        description=charge.description,
        valid_from=charge.valid_from,
        valid_to=charge.valid_to,
        price1=charge.price1,
        price2=charge.price2,
        price3=charge.price3,
        price4=charge.price4,
        price5=charge.price5,
        price6=charge.price6,
        price7=charge.price7,
        price8=charge.price8,
        price9=charge.price9,
        price10=charge.price10,
        price11=charge.price11,
        price12=charge.price12,
        price13=charge.price13,
        price14=charge.price14,
        price15=charge.price15,
        price16=charge.price16,
        price17=charge.price17,
        price18=charge.price18,
        price19=charge.price19,
        price20=charge.price20,
        price21=charge.price21,
        price22=charge.price22,
        price23=charge.price23,
        price24=charge.price24,
        created_at=charge.created_at,
        error=_error,
    )

    return my_charge


async def delete_charge(data, session):
    charge = session.query(Charge).filter(Charge.id == data).first()
    if not charge:
        raise HTTPException(status_code=404, detail="Charge not found.")
    session.delete(charge)
    session.commit()
    return {"message": "Charge deleted successfully."}


async def add_charge(data, session):
    chargeowner = session.query(Chargeowner).filter(Chargeowner.id == data.chargeowner_id).first()
    if not chargeowner:
        raise HTTPException(status_code=404, detail="Charge owner not found.")

    existing_charge = (
        session.query(Charge)
        .filter(
            and_(
                Charge.chargeowner_id == data.chargeowner_id,
                or_(
                    and_(Charge.valid_from <= data.valid_from, Charge.valid_to > data.valid_from),
                    and_(Charge.valid_from < data.valid_to, Charge.valid_to >= data.valid_to),
                ),
            )
        )
        .first()
    )

    if existing_charge:
        raise HTTPException(status_code=404, detail="A charge already exists within the specified date range.")

    charge = Charge()
    charge.chargeowner_id = data.chargeowner_id
    charge.charge_type = data.charge_type
    charge.charge_type_code = data.charge_type_code
    charge.note = data.note
    charge.description = data.description
    charge.valid_from = data.valid_from
    charge.valid_to = data.valid_to
    charge.price1 = data.price1
    charge.price2 = data.price2
    charge.price3 = data.price3
    charge.price4 = data.price4
    charge.price5 = data.price5
    charge.price6 = data.price6
    charge.price7 = data.price7
    charge.price8 = data.price8
    charge.price9 = data.price9
    charge.price10 = data.price10
    charge.price11 = data.price11
    charge.price12 = data.price12
    charge.price13 = data.price13
    charge.price14 = data.price14
    charge.price15 = data.price15
    charge.price16 = data.price16
    charge.price17 = data.price17
    charge.price18 = data.price18
    charge.price19 = data.price19
    charge.price20 = data.price20
    charge.price21 = data.price21
    charge.price22 = data.price22
    charge.price23 = data.price23
    charge.price24 = data.price24
    charge.created_at = datetime.now(timezone.utc)
    session.add(charge)
    session.commit()
    session.refresh(charge)

    return await fetch_charge_details(charge.id, session)


async def fetch_charges_for_date_and_gln(session, qdate, chargeowner_glnnumber):
    chargeowner = session.query(Chargeowner).filter(Chargeowner.glnnumber == chargeowner_glnnumber).first()
    if not chargeowner:
        raise HTTPException(status_code=404, detail="Charge owner not found.")

    charge = (
        session.query(Charge)
        .filter(and_(Charge.valid_from <= qdate, Charge.valid_to > qdate, Charge.chargeowner_id == chargeowner.id))
        .first()
    )

    if not charge:
        raise HTTPException(status_code=404, detail="No charges found.")

    my_charge = ChargeResponse(
        id=charge.id,
        chargeowner_id=charge.chargeowner_id,
        charge_type=charge.charge_type,
        charge_type_code=charge.charge_type_code,
        note=charge.note,
        description=charge.description,
        valid_from=charge.valid_from,
        valid_to=charge.valid_to,
        price1=charge.price1,
        price2=charge.price2,
        price3=charge.price3,
        price4=charge.price4,
        price5=charge.price5,
        price6=charge.price6,
        price7=charge.price7,
        price8=charge.price8,
        price9=charge.price9,
        price10=charge.price10,
        price11=charge.price11,
        price12=charge.price12,
        price13=charge.price13,
        price14=charge.price14,
        price15=charge.price15,
        price16=charge.price16,
        price17=charge.price17,
        price18=charge.price18,
        price19=charge.price19,
        price20=charge.price20,
        price21=charge.price21,
        price22=charge.price22,
        price23=charge.price23,
        price24=charge.price24,
        created_at=charge.created_at,
    )
    return my_charge


async def fetch_charges_for_chargeowner(session, chargeowner_glnnumber):
    chargeowner = session.query(Chargeowner).filter(Chargeowner.glnnumber == chargeowner_glnnumber).first()
    if not chargeowner:
        raise HTTPException(status_code=404, detail="Charge owner not found.")

    charges = session.query(Charge).filter(Charge.chargeowner_id == chargeowner.id).order_by(Charge.valid_from).all()

    if not charges:
        raise HTTPException(status_code=404, detail="No charges found.")

    my_charges = []

    for charge in charges:
        my_charges.append(
            ChargeResponse(
                id=charge.id,
                chargeowner_id=charge.chargeowner_id,
                charge_type=charge.charge_type,
                charge_type_code=charge.charge_type_code,
                note=charge.note,
                description=charge.description,
                valid_from=charge.valid_from,
                valid_to=charge.valid_to,
                price1=charge.price1,
                price2=charge.price2,
                price3=charge.price3,
                price4=charge.price4,
                price5=charge.price5,
                price6=charge.price6,
                price7=charge.price7,
                price8=charge.price8,
                price9=charge.price9,
                price10=charge.price10,
                price11=charge.price11,
                price12=charge.price12,
                price13=charge.price13,
                price14=charge.price14,
                price15=charge.price15,
                price16=charge.price16,
                price17=charge.price17,
                price18=charge.price18,
                price19=charge.price19,
                price20=charge.price20,
                price21=charge.price21,
                price22=charge.price22,
                price23=charge.price23,
                price24=charge.price24,
                created_at=charge.created_at,
            )
        )
    return my_charges
