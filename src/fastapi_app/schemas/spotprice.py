from datetime import datetime

from pydantic import BaseModel


class AddSpotpriceRequest(BaseModel):
    HourUTC: str
    HourDK: str
    PriceArea: str
    SpotpriceDKK: float


class MultiAreaEntry(BaseModel):
    deliveryStart: datetime
    deliveryEnd: datetime
    entryPerArea: dict[str, float]


class PriceRequest(BaseModel):
    deliveryDateCET: str
    version: int
    updatedAt: str
    deliveryAreas: list[str]
    deliveryAreas: list[str]
    market: str
    multiAreaEntries: list[MultiAreaEntry]
