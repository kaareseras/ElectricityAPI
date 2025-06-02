from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from sqlalchemy import Date
from sqlmodel import func

from src.fastapi_app.config.config import get_settings
from src.fastapi_app.models.spotprice import Spotprice
from src.fastapi_app.responses.spotprice import SpotpriceResponse
from src.fastapi_app.schemas.spotprice import PriceRequest

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
    if qdate is None:
        copenhagen_tz = ZoneInfo("Europe/Copenhagen")
        qdate = datetime.now(copenhagen_tz).replace(hour=0, minute=0, second=0, microsecond=0)

    if isinstance(qdate, datetime):
        qdate = qdate.date()

    spotprices = (
        session.query(Spotprice).filter(func.date(Spotprice.DateDK) == qdate, Spotprice.PriceArea == pricearea).all()
    )

    if not spotprices:
        raise HTTPException(status_code=404, detail=f"No spotprices found for date {qdate} and area {pricearea}.")

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


# This function processes a PriceRequest and loads spot prices into the database.
# It converts the delivery times from UTC to Copenhagen time, and creates Spotprice entries for each area.
# It returns the number of entries inserted into the database.


async def load_spot_prices(data: PriceRequest, session) -> int:
    copenhagen = ZoneInfo("Europe/Copenhagen")
    entries: list[Spotprice] = []
    for entry in data.multiAreaEntries:
        hour_utc = entry.deliveryStart
        hour_dk = hour_utc.astimezone(copenhagen)
        date_dk = hour_dk.date()

        # Dividing price with 1000 to convert from kr/MWh to kr/kWh
        for area, price in entry.entryPerArea.items():
            entries.append(
                Spotprice(HourUTC=hour_utc, HourDK=hour_dk, DateDK=date_dk, PriceArea=area, SpotpriceDKK=price / 1000)
            )

    session.add_all(entries)
    session.commit()
    return len(entries)
