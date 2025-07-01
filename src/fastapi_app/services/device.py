from datetime import UTC, datetime
from zoneinfo import ZoneInfo

import pandas as pd
from fastapi import HTTPException
from pandas import Timestamp
from sqlalchemy import Date

from src.fastapi_app.config.config import get_settings
from src.fastapi_app.models.chargeowner import Chargeowner
from src.fastapi_app.models.device import Device
from src.fastapi_app.responses.dayprice import DaypriceResponse, hourPrice
from src.fastapi_app.schemas.device import AddDeviceRequest, AdoptDeviceRequest
from src.fastapi_app.services.charge import fetch_charges_for_date_and_gln
from src.fastapi_app.services.chargeowner import fetch_chargeowner_details
from src.fastapi_app.services.spotprice import fetch_spotprices_for_date
from src.fastapi_app.services.tarif import fetch_tarif_by_date
from src.fastapi_app.services.tax import fetch_tax_by_date

settings = get_settings()


async def fetch_device_details(uuid, session, user):
    device = session.query(Device).filter(Device.uuid == uuid and Device.user_id == user.id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found.")

    return {
        "uuid": device.uuid,
        "user_id": device.user_id,
        "name": device.name,
        "chargeowner_id": device.chargeowner_id,
        "price_area": device.price_area,
        "is_electric_heated": device.is_electric_heated,
        "config": device.config,
        "devicetype_id": device.devicetype_id,
        "retail_markup": device.retail_markup,
        "last_activity": device.last_activity,
        "created_at": device.created_at,
        "is_adopted": device.is_adopted,
        "adopted_at": device.adopted_at,
        "is_blocked": device.is_blocked,
        "blocked_at": device.blocked_at,
    }


"""
Only user is needed to fetch device details without user context.
This is useful for admin operations or when the user context is not available 
like when a device is requesting its prices.
"""


async def fetch_device_details_no_user(uuid, session):
    device = session.query(Device).filter(Device.uuid == uuid).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found.")

    return {
        "uuid": device.uuid,
        "user_id": device.user_id,
        "name": device.name,
        "chargeowner_id": device.chargeowner_id,
        "price_area": device.price_area,
        "is_electric_heated": device.is_electric_heated,
        "config": device.config,
        "devicetype_id": device.devicetype_id,
        "retail_markup": device.retail_markup,
        "last_activity": device.last_activity,
        "created_at": device.created_at,
        "is_adopted": device.is_adopted,
        "adopted_at": device.adopted_at,
        "is_blocked": device.is_blocked,
        "blocked_at": device.blocked_at,
    }


async def fetch_devices_for_user(session, user):
    devices = session.query(Device).filter(Device.user_id == user.id).all()
    if not devices:
        raise HTTPException(status_code=404, detail="No devices found.")

    return [
        {
            "uuid": device.uuid,
            "user_id": device.user_id,
            "name": device.name,
            "chargeowner_id": device.chargeowner_id,
            "price_area": device.price_area,
            "is_electric_heated": device.is_electric_heated,
            "config": device.config,
            "devicetype_id": device.devicetype_id,
            "retail_markup": device.retail_markup,
            "last_activity": device.last_activity,
            "created_at": device.created_at,
            "is_adopted": device.is_adopted,
            "adopted_at": device.adopted_at,
            "is_blocked": device.is_blocked,
            "blocked_at": device.blocked_at,
        }
        for device in devices
    ]


async def fetch_devices(session):
    devices = session.query(Device).all()
    if not devices:
        raise HTTPException(status_code=404, detail="No devices found.")

    return [
        {
            "uuid": device.uuid,
            "user_id": device.user_id,
            "name": device.name,
            "chargeowner_id": device.chargeowner_id,
            "price_area": device.price_area,
            "is_electric_heated": device.is_electric_heated,
            "config": device.config,
            "devicetype_id": device.devicetype_id,
            "retail_markup": device.retail_markup,
            "last_activity": device.last_activity,
            "created_at": device.created_at,
            "is_adopted": device.is_adopted,
            "adopted_at": device.adopted_at,
            "is_blocked": device.is_blocked,
            "blocked_at": device.blocked_at,
        }
        for device in devices
    ]


async def delete_device(uuid, session, user):
    device = session.query(Device).filter(Device.uuid == uuid and Device.user_id == user.id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found.")

    session.delete(device)
    session.commit()
    return {"message": "Device deleted successfully."}


async def add_device(data: AddDeviceRequest, session):
    # Check if the device already exists
    existing = session.get(Device, data.uuid)
    if existing:
        raise HTTPException(status_code=404, detail="Device already exists.")

    # Add new device
    device = Device(
        uuid=data.uuid,
        name=data.name,
        is_electric_heated=data.is_electric_heated,
        last_activity=datetime.now(UTC),
        created_at=datetime.now(UTC),
        is_adopted=False,
        is_blocked=False,
        adopted_at=None,
        blocked_at=None,
    )
    session.add(device)
    session.commit()
    session.refresh(device)

    return device


async def adopt_device(data: AdoptDeviceRequest, session, user):
    device = session.query(Device).filter(Device.uuid == data.uuid and Device.user_id == user.id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found.")
    if device.is_adopted:
        raise HTTPException(status_code=400, detail="Device already adopted.")
    chargeowner = session.query(Chargeowner).filter(Chargeowner.id == data.chargeowner_id).first()
    if not chargeowner:
        raise HTTPException(status_code=404, detail="Charge owner not found.")
    if data.price_area not in ["DK1", "DK2"]:
        raise HTTPException(status_code=400, detail="Invalid PriceArea. Must be 'DK1' or 'DK2'.")

    device.name = data.name if data.name else device.uuid
    device.chargeowner_id = data.chargeowner_id
    device.price_area = data.price_area
    device.is_electric_heated = data.is_electric_heated
    device.user_id = user.id
    device.is_adopted = True
    device.adopted_at = datetime.now(UTC)

    session.commit()
    session.refresh(device)

    return device


async def update_device(device_uuid, data, session, user):
    device = session.query(Device).filter(Device.uuid == device_uuid and Device.user_id == user.id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found.")

    device.uuid = data.uuid
    device.name = data.name
    device.chargeowner_id = data.chargeowner_id
    device.price_area = data.price_area
    device.is_electric_heated = data.is_electric_heated
    device.config = data.config
    device.devicetype_id = data.devicetype_id
    device.retail_markup = data.retail_markup if data.retail_markup is not None else device.retail_markup
    device.last_activity = datetime.now(UTC)
    device.updated_at = datetime.now(UTC)

    session.commit()
    session.refresh(device)

    return await fetch_device_details(device.uuid, session, user)


async def fetch_device_dayprice(uuid: str, qdate: Date, session):
    # Set Danish timezone
    tz = ZoneInfo("Europe/Copenhagen")

    # Ensure the qdate is a timezone-aware Timestamp in Europe/Copenhagen
    ts = Timestamp(qdate)
    if ts.tzinfo is None:
        start = ts.tz_localize(tz)
    else:
        start = ts.tz_convert(tz)

    # Create hourly range for the date
    hour_range = pd.date_range(start=start.date(), periods=24, freq="h")

    # Fetch device and related data
    device = await fetch_device_details_no_user(uuid, session)
    chargeowner = await fetch_chargeowner_details(device["chargeowner_id"], session)
    spotprices = await fetch_spotprices_for_date(session, qdate, device["price_area"])
    tax = await fetch_tax_by_date(qdate, session)
    tarif = await fetch_tarif_by_date(qdate, session)
    charge = await fetch_charges_for_date_and_gln(session, qdate, chargeowner.glnnumber)

    # Build initial DataFrame
    df = pd.DataFrame({"HourDK": hour_range})

    # Create DataFrame from spot prices
    spotprice_df = pd.DataFrame([{"HourDK": sp.HourDK, "SpotPrice": sp.SpotpriceDKK} for sp in spotprices])

    # Ensure HourDK is timezone-aware and in correct tz
    spotprice_df["HourDK"] = pd.to_datetime(spotprice_df["HourDK"])

    # Merge with spot prices
    df = df.merge(spotprice_df, on="HourDK", how="left")

    # Create charge DataFrame using same hour_range
    charge_df = pd.DataFrame(
        {
            "HourDK": hour_range,
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
    )

    # Merge with charge data
    df = df.merge(charge_df, on="HourDK", how="left")

    # Add tax and tarif (applying VAT if needed)
    df["Tax"] = tax.taxammount * (1.25 if not tax.includingVAT else 1)
    df["NetTarif"] = tarif.nettarif * (1.25 if not tarif.includingVAT else 1)
    df["SystemTarif"] = tarif.systemtarif * (1.25 if not tarif.includingVAT else 1)

    # Calculate total price and add VAT for Spotprice and charge
    df["TotalPrice"] = (
        df["SpotPrice"] * 1.25 + df["Charge"] * 1.25 + df["Tax"] + df["NetTarif"] + df["SystemTarif"]
    ).round(3)

    print(df)

    # Find max/min for flagging
    max_price = df["TotalPrice"].max()
    min_price = df["TotalPrice"].min()

    # Build response
    _prices = [
        hourPrice(
            hour=row["HourDK"].to_pydatetime() if hasattr(row["HourDK"], "to_pydatetime") else row["HourDK"],
            totalprice=float(row["TotalPrice"]),
            spotprice=float(row["SpotPrice"]),
            isMax=bool(row["TotalPrice"] == max_price),
            isMin=bool(row["TotalPrice"] == min_price),
        )
        for _, row in df.iterrows()
    ]

    return DaypriceResponse(qdate=qdate, uuid=device["uuid"], prices=_prices)
