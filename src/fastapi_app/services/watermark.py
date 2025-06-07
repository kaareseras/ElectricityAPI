from datetime import datetime

from src.fastapi_app.models.charge import Charge
from src.fastapi_app.models.spotprice import Spotprice
from src.fastapi_app.models.tarif import Tarif
from src.fastapi_app.models.tax import Tax
from src.fastapi_app.responses.watermark import WatermarkResponse


async def fetch_watermark(session):
    """Fetches the latest dates for spot prices, charges, taxes, and tariffs from the database.
    Args:
        session: SQLAlchemy session to interact with the database.
    Returns:
        WatermarkResponse: An object containing the latest dates for spot prices, charges, taxes, and tariffs.
    """

    taxes_max_date = None
    spotprices_max_date = None
    tarifs_max_date = None
    charges_max_date = None

    tax = session.query(Tax).order_by(Tax.created_at.desc()).first()
    if tax:
        taxes_max_date = tax.created_at
    else:
        taxes_max_date = datetime.now()

    spotprice = session.query(Spotprice).order_by(Spotprice.DateDK.desc()).first()
    if spotprice:
        spotprices_max_date = spotprice.DateDK
    else:
        spotprices_max_date = datetime.now()

    tarif = session.query(Tarif).order_by(Tarif.created_at.desc()).first()
    if tarif:
        tarifs_max_date = tarif.created_at
    else:
        tarifs_max_date = datetime.now()

    charge = session.query(Charge).order_by(Charge.created_at.desc()).first()
    if charge:
        charges_max_date = charge.created_at
    else:
        charges_max_date = datetime.now()

    my_watermark = WatermarkResponse(
        spotprices_max_date=spotprices_max_date,
        charges_max_date=charges_max_date,
        taxes_max_date=taxes_max_date,
        tarifs_max_date=tarifs_max_date,
    )

    return my_watermark
