from fastapi import HTTPException
from sqlalchemy import and_, or_

from src.fastapi_app.config.config import get_settings
from src.fastapi_app.models.tax import Tax
from src.fastapi_app.responses.tax import TaxResponse

settings = get_settings()


async def fetch_tax_details(data, session):
    tax = session.query(Tax).filter(Tax.id == data).first()
    _error = ""
    if not tax:
        raise HTTPException(status_code=404, detail="Tax not found.")

    my_tax = TaxResponse(
        id=tax.id,
        valid_from=tax.valid_from,
        valid_to=tax.valid_to,
        taxammount=tax.taxammount,
        includingVAT=tax.includingVAT,
        created_at=tax.created_at,
        error=_error,
    )

    return my_tax


async def fetch_tax_by_date(qdate, session):
    tax = session.query(Tax).filter(and_(Tax.valid_from <= qdate, Tax.valid_to > qdate)).first()
    _error = ""
    if not tax:
        raise HTTPException(status_code=404, detail="Tax not found.")

    my_tax = TaxResponse(
        id=tax.id,
        valid_from=tax.valid_from,
        valid_to=tax.valid_to,
        taxammount=tax.taxammount,
        includingVAT=tax.includingVAT,
        created_at=tax.created_at,
        error=_error,
    )

    return my_tax


async def fetch_taxes(session):
    taxes = session.query(Tax).order_by(Tax.valid_from).all()
    _error = ""
    if not taxes:
        raise HTTPException(status_code=404, detail="Tax not found.")

    my_taxes = []
    for tax in taxes:
        my_tax = TaxResponse(
            id=tax.id,
            valid_from=tax.valid_from,
            valid_to=tax.valid_to,
            taxammount=tax.taxammount,
            includingVAT=tax.includingVAT,
            created_at=tax.created_at,
            error=_error,
        )
        my_taxes.append(my_tax)

    return my_taxes


async def delete_tax(pk, session):
    tax = session.query(Tax).filter(Tax.id == pk).first()
    if not tax:
        raise HTTPException(status_code=404, detail="Tax not found.")
    session.delete(tax)
    session.commit()
    return {"message": "Tax deleted successfully."}


async def upsert_tax(data, session):
    new_tax = Tax()
    new_tax.valid_from = data.valid_from
    new_tax.valid_to = data.valid_to
    new_tax.taxammount = data.taxammount
    new_tax.includingVAT = data.includingVAT

    existing_tax = (
        session.query(Tax)
        .filter(
            or_(
                and_(Tax.valid_from <= data.valid_from, Tax.valid_to > data.valid_from),
                and_(Tax.valid_from < data.valid_to, Tax.valid_to >= data.valid_to),
            )
        )
        .first()
    )

    # If the latest tax is None, it means there are no taxes
    if not existing_tax:
        session.add(new_tax)
        session.commit()
        session.refresh(new_tax)
        return await fetch_tax_details(new_tax.id, session)

    # If the new tax's valid_from  is after the existing tax's valid_from
    # meaning its a newer tax, we can update the existing tax's valid_to
    # and add the new tax
    elif existing_tax.valid_from < new_tax.valid_from:
        existing_tax.valid_to = new_tax.valid_from
        session.add(new_tax)
        session.commit()
        session.refresh(new_tax)
        return await fetch_tax_details(new_tax.id, session)

    # if the current tax is still applicable
    else:
        raise HTTPException(status_code=404, detail="A tax already exists within the specified date range.")
