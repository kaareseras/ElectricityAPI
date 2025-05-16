from datetime import datetime, timezone

import pandas as pd
from fastapi import HTTPException
from sqlalchemy import Date

from src.fastapi_app.config.config import get_settings
from src.fastapi_app.models.device import Device
from src.fastapi_app.responses.dayprice import DaypriceResponse, hourPrice
from src.fastapi_app.services.charge import fetch_charges_for_date_and_gln
from src.fastapi_app.services.chargeowner import fetch_chargeowner_details
from src.fastapi_app.services.spotprice import fetch_spotprices_for_date
from src.fastapi_app.services.tarif import fetch_tarif_by_date
from src.fastapi_app.services.tax import fetch_tax_by_date

settings = get_settings()


async def fetch_device_details(uuid, session):
    device = session.query(Device).filter(Device.uuid == uuid).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found.")

    return {
        "uuid": device.uuid,
        "chargeowner_id": device.chargeowner_id,
        "PriceArea": device.PriceArea,
        "Config": device.Config,
        "last_activity": device.last_activity,
        "created_at": device.created_at,
    }


async def fetch_devices(session):
    devices = session.query(Device).all()
    if not devices:
        raise HTTPException(status_code=404, detail="No devices found.")

    return [
        {
            "uuid": device.uuid,
            "chargeowner_id": device.chargeowner_id,
            "PriceArea": device.PriceArea,
            "Config": device.Config,
            "last_activity": device.last_activity,
            "created_at": device.created_at,
        }
        for device in devices
    ]


async def delete_device(uuid, session):
    device = session.query(Device).filter(Device.uuid == uuid).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found.")

    session.delete(device)
    session.commit()
    return {"message": "Device deleted successfully."}


async def add_device(data, session):
    try:
        device = Device(uuid=data.uuid, last_activity=datetime.now(timezone.utc), created_at=datetime.now(timezone.utc))
        session.add(device)
        session.commit()
        session.refresh(device)
    except Exception:
        raise HTTPException(status_code=404, detail="Device not added.")

    return await fetch_device_details(device.uuid, session)


async def update_device(device_uuid, data, session):
    device = session.query(Device).filter(Device.uuid == device_uuid).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found.")

    device.uuid = data.uuid
    device.chargeowner_id = data.chargeowner_id
    device.PriceArea = data.PriceArea
    device.Config = data.Config
    device.last_activity = datetime.now(timezone.utc)
    device.updated_at = datetime.now(timezone.utc)

    session.commit()
    session.refresh(device)

    return await fetch_device_details(device.uuid, session)


async def fetch_device_dayprice(uuid: str, qdate: Date, session):
    # Fetch the device details

    device = await fetch_device_details(uuid, session)

    chargeowner = await fetch_chargeowner_details(device["chargeowner_id"], session)

    # Fetch the spot prices for the specified date and price area

    spotprices = await fetch_spotprices_for_date(session, qdate, device["PriceArea"])

    # Fetch the tax and tarif data for the specified date

    tax = await fetch_tax_by_date(qdate, session)

    tarif = await fetch_tarif_by_date(qdate, session)

    charge = await fetch_charges_for_date_and_gln(session, qdate, chargeowner.glnnumber)

    # Create a DataFrame with a column 'HourDK' containing hourly timestamps starting from the current day
    df = pd.DataFrame({"HourDK": pd.date_range(start=qdate, periods=24, freq="h")})

    # Create a DataFrame from the spot prices
    spotprice_df = pd.DataFrame([{"HourDK": sp.HourDK, "SpotPrice": sp.SpotpriceDKK} for sp in spotprices])

    # Merge the spot price DataFrame with the existing DataFrame on the 'Hour' column
    df = df.merge(spotprice_df, on="HourDK", how="left")

    # Create a DataFrame from the charge model
    charge_data = {
        "HourDK": pd.date_range(start=qdate, periods=24, freq="h"),
        "Charge": [
            charge.price1,
            charge.price2,
            charge.price3,
            charge.price4,
            charge.price5,
            charge.price6,
            charge.price7,
            charge.price8,
            charge.price9,
            charge.price10,
            charge.price11,
            charge.price12,
            charge.price13,
            charge.price14,
            charge.price15,
            charge.price16,
            charge.price17,
            charge.price18,
            charge.price19,
            charge.price20,
            charge.price21,
            charge.price22,
            charge.price23,
            charge.price24,
        ],
    }

    charge_df = pd.DataFrame(charge_data)

    # Merge the charge DataFrame with the existing DataFrame on the 'HourDK' column
    df = df.merge(charge_df, on="HourDK", how="left")

    # Add the tax and tarif data with the existing DataFrame
    if not tax.includingVAT:
        tax.taxammount = tax.taxammount * 1.25
    df["Tax"] = tax.taxammount

    if not tarif.includingVAT:
        tarif.nettarif = tarif.nettarif * 1.25
        tarif.systemtarif = tarif.systemtarif * 1.25
    df["NetTarif"] = tarif.nettarif
    df["SystemTarif"] = tarif.systemtarif

    # Calculate the total cost per hour
    df["TotalPrice"] = (df["SpotPrice"] + df["Charge"] + df["Tax"] + df["NetTarif"] + df["SystemTarif"]).round(3)

    # Build the response object

    _prices = []

    for index, row in df.iterrows():
        _prices.append(
            hourPrice(
                hour=row["HourDK"],
                totalprice=row["TotalPrice"],
                spotprice=row["SpotPrice"],
                isMax=row["TotalPrice"] == df["TotalPrice"].max(),
                isMin=row["TotalPrice"] == df["TotalPrice"].min(),
            )
        )

    response = DaypriceResponse(qdate=qdate, uuid=device["uuid"], prices=_prices)

    return response
