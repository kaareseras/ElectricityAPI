from datetime import datetime, timezone

from fastapi import HTTPException
from pytz import timezone as pytz_timezone
from sqlalchemy import Date, and_

from src.fastapi_app.config.config import get_settings
from src.fastapi_app.models.spotprice import Spotprice
from src.fastapi_app.responses.spotprice import SpotpriceResponse

settings = get_settings()


async def fetch_spotprice_details(data, session):
    spotprice = session.query(Spotprice).filter(Spotprice.id == data).first()
    _error = ""
    if not spotprice:
        raise HTTPException(status_code=404, detail="Spotprice not found.")

    my_spotprice = SpotpriceResponse(
        id=spotprice.id,
        HourUTC=spotprice.HourUTC,
        HourDK=spotprice.HourDK,
        PriceArea=spotprice.PriceArea,
        SpotpriceDKK=spotprice.SpotpriceDKK,
        created_at=spotprice.created_at,
        error=_error,
    )

    return my_spotprice


async def delete_spotprice(data, session):
    spotprice = session.query(Spotprice).filter(Spotprice.id == data).first()
    if not spotprice:
        raise HTTPException(status_code=404, detail="Chargeowner not found.")
    session.delete(spotprice)
    session.commit()
    return {"message": "Spotprice deleted successfully."}


async def delete_all_spotprices(session):
    spotprices = session.query(Spotprice).all()
    if not spotprices:
        raise HTTPException(status_code=404, detail="No spotprices found.")
    for spotprice in spotprices:
        session.delete(spotprice)
    session.commit()
    return {"message": "All spotprices deleted successfully."}


async def add_spotprice(data, session):
    spotprice = Spotprice()
    spotprice.HourUTC = datetime.strptime(data.HourUTC, "%Y-%m-%dT%H:%M:%S")
    spotprice.HourDK = datetime.strptime(data.HourDK, "%Y-%m-%dT%H:%M:%S")
    spotprice.DateDK = spotprice.HourDK.date()
    spotprice.PriceArea = data.PriceArea
    spotprice.SpotpriceDKK = data.SpotpriceDKK
    spotprice.created_at = datetime.now(timezone.utc)
    session.add(spotprice)
    session.commit()
    session.refresh(spotprice)

    return await fetch_spotprice_details(spotprice.id, session)


async def add_spotprices(data_list, session):
    spotprices = []
    for data in data_list:
        spotprice = Spotprice()
        spotprice.HourUTC = datetime.strptime(data.HourUTC, "%Y-%m-%dT%H:%M:%S")
        spotprice.HourDK = datetime.strptime(data.HourDK, "%Y-%m-%dT%H:%M:%S")
        spotprice.DateDK = spotprice.HourDK.date()
        spotprice.PriceArea = data.PriceArea
        spotprice.SpotpriceDKK = data.SpotpriceDKK
        spotprice.created_at = datetime.now(timezone.utc)
        session.add(spotprice)
        spotprices.append(spotprice)

    session.commit()

    for spotprice in spotprices:
        session.refresh(spotprice)

    return await fetch_spotprices(session)


async def fetch_spotprices(session):
    spotprices = session.query(Spotprice).all()

    my_spotprices = []

    if not spotprices:
        raise HTTPException(status_code=404, detail="No spotprices found.")

    for spotprice in spotprices:
        my_spotprices.append(
            SpotpriceResponse(
                id=spotprice.id,
                HourUTC=spotprice.HourUTC,
                HourDK=spotprice.HourDK,
                PriceArea=spotprice.PriceArea,
                SpotpriceDKK=spotprice.SpotpriceDKK,
                created_at=spotprice.created_at,
            )
        )
    return my_spotprices


async def fetch_spotprices_for_date(session, qdate: Date, pricearea: str):
    if qdate == None:
        copenhagen_tz = pytz_timezone("Europe/Copenhagen")
        qdate = datetime.now(copenhagen_tz).replace(hour=0, minute=0, second=0, microsecond=0)

    spotprices = (
        session.query(Spotprice).filter(and_(Spotprice.DateDK == qdate, Spotprice.PriceArea == pricearea)).all()
    )

    if not spotprices:
        raise HTTPException(status_code=404, detail="No spotprices found.")

    my_spotprices = []

    for spotprice in spotprices:
        my_spotprices.append(
            SpotpriceResponse(
                id=spotprice.id,
                HourUTC=spotprice.HourUTC,
                HourDK=spotprice.HourDK,
                PriceArea=spotprice.PriceArea,
                SpotpriceDKK=spotprice.SpotpriceDKK,
                created_at=spotprice.created_at,
            )
        )
    return my_spotprices
