from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import and_, or_

from src.fastapi_app.config.config import get_settings
from src.fastapi_app.models.charge import Charge
from src.fastapi_app.models.chargeowner import Chargeowner
from src.fastapi_app.responses.charge import ChargeResponse
from src.fastapi_app.utils.agregate_charge import aggregate_charges
from src.fastapi_app.utils.chargecompare import compare_charges

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


async def upsert_charge(data, session):
    # Use a far future date as a default
    FUTURE_DATE = datetime(9999, 12, 31, 23, 59, 59)

    chargeowner = session.query(Chargeowner).filter(Chargeowner.id == data.chargeowner_id).first()
    if not chargeowner:
        raise HTTPException(status_code=404, detail="Charge owner not found.")

    new_charge = Charge()
    new_charge.chargeowner_id = data.chargeowner_id
    new_charge.charge_type = data.charge_type
    new_charge.charge_type_code = data.charge_type_code
    new_charge.note = data.note
    new_charge.description = data.description
    new_charge.valid_from = data.valid_from
    new_charge.valid_to = data.valid_to
    new_charge.price1 = data.price1
    new_charge.price2 = data.price2
    new_charge.price3 = data.price3
    new_charge.price4 = data.price4
    new_charge.price5 = data.price5
    new_charge.price6 = data.price6
    new_charge.price7 = data.price7
    new_charge.price8 = data.price8
    new_charge.price9 = data.price9
    new_charge.price10 = data.price10
    new_charge.price11 = data.price11
    new_charge.price12 = data.price12
    new_charge.price13 = data.price13
    new_charge.price14 = data.price14
    new_charge.price15 = data.price15
    new_charge.price16 = data.price16
    new_charge.price17 = data.price17
    new_charge.price18 = data.price18
    new_charge.price19 = data.price19
    new_charge.price20 = data.price20
    new_charge.price21 = data.price21
    new_charge.price22 = data.price22
    new_charge.price23 = data.price23
    new_charge.price24 = data.price24
    new_charge.created_at = datetime.now(timezone.utc)

    # Check if there is an existing charge for the same owner and type within the date range
    existing_charge: Charge = (
        session.query(Charge)
        .filter(
            and_(
                Charge.chargeowner_id == new_charge.chargeowner_id,
                Charge.charge_type_code == new_charge.charge_type_code,
                or_(
                    and_(Charge.valid_from <= new_charge.valid_from, Charge.valid_to > new_charge.valid_from),
                    and_(Charge.valid_from < new_charge.valid_to, Charge.valid_to >= new_charge.valid_to),
                ),
            )
        )
        .first()
    )

    # Get latest existing tariff for this owner
    latest_charge: Charge = (
        session.query(Charge)
        .filter(Charge.chargeowner_id == new_charge.chargeowner_id)
        .order_by(Charge.valid_from.desc())
        .limit(1)
        .first()
    )

    # If the latest charge is None, it means there are no charges for this owner
    if not latest_charge:
        # If no existing charge found, add the new charge
        session.add(new_charge)
        session.commit()
        session.refresh(new_charge)
        return await fetch_charge_details(new_charge.id, session)

    # If the new charge is the same as the latest charge, update the existing charge and return the updated charge
    elif not existing_charge and compare_charges(latest_charge, new_charge):
        latest_charge.valid_to = new_charge.valid_to
        session.commit()
        session.refresh(latest_charge)
        return await fetch_charge_details(latest_charge.id, session)

    # If the new charge is different from the latest charge, check if it overlaps with any existing charges
    # insert the new record
    elif not existing_charge and not compare_charges(latest_charge, new_charge):
        # If no existing charge found, add the new charge
        session.add(new_charge)
        session.commit()
        session.refresh(new_charge)
        return await fetch_charge_details(new_charge.id, session)

    # If an existing charge is found, but it has a defult end date, check if the new charge starts after the existing charge
    # and if it does stop the existing charge and insert the new one
    elif (
        existing_charge
        and existing_charge.valid_to == FUTURE_DATE
        and new_charge.valid_from > existing_charge.valid_from
    ):
        existing_charge.valid_to = new_charge.valid_from
        session.add(new_charge)
        session.commit()
        session.refresh(new_charge)
        return await fetch_charge_details(new_charge.id, session)

    # In any other case, dont insert the reccord or update anything
    else:
        raise HTTPException(
            status_code=404,
            detail=(
                "A charge with the same type and code already exists for this charge owner "
                "within the specified date range."
            ),
        )


async def fetch_charges_for_date_and_gln(session, qdate, chargeowner_glnnumber):
    chargeowner = session.query(Chargeowner).filter(Chargeowner.glnnumber == chargeowner_glnnumber).first()
    if not chargeowner:
        raise HTTPException(status_code=404, detail="Charge owner not found.")

    charges = (
        session.query(Charge)
        .filter(and_(Charge.valid_from <= qdate, Charge.valid_to > qdate, Charge.chargeowner_id == chargeowner.id))
        .all()
    )

    if not charges:
        raise HTTPException(status_code=404, detail="No charges found.")

    # If there is only one charge, use it directly
    if len(charges) == 1:
        charge = charges[0]
    else:
        # Aggregate charges if there are multiple charges for the same date and GLN
        charge = aggregate_charges(charges)

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


async def fetch_charges_for_chargeowner_by_gln(session, chargeowner_glnnumber):
    chargeowner = session.query(Chargeowner).filter(Chargeowner.glnnumber == chargeowner_glnnumber).first()
    if not chargeowner:
        raise HTTPException(status_code=404, detail="Charge owner not found.")

    return await fetch_charges_for_chargeowner(session, chargeowner.id)


async def fetch_charges_for_chargeowner(session, id):
    chargeowner = session.query(Chargeowner).filter(Chargeowner.id == id).first()
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
