from datetime import datetime

from src.fastapi_app.schemas.base import BaseSchema


class AddSpotpriceRequest(BaseSchema):
    HourUTC: str
    HourDK: str
    PriceArea: str
    SpotpriceDKK: float


class MultiAreaEntry(BaseSchema):
    deliveryStart: datetime
    deliveryEnd: datetime
    entryPerArea: dict[str, float]


class PriceRequest(BaseSchema):
    deliveryDateCET: str
    version: int
    updatedAt: str
    deliveryAreas: list[str]
    deliveryAreas: list[str]
    market: str
    multiAreaEntries: list[MultiAreaEntry]
