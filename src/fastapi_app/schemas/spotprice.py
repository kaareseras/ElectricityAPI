from pydantic import BaseModel


class AddSpotpriceRequest(BaseModel):
    HourUTC: str
    HourDK: str
    PriceArea: str
    SpotpriceDKK: float
