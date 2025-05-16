from datetime import datetime
from typing import Union

from src.fastapi_app.responses.base import BaseResponse


class SpotpriceResponse(BaseResponse):
    id: int
    HourUTC: Union[str, None, datetime] = None
    HourDK: Union[str, None, datetime] = None
    PriceArea: str
    SpotpriceDKK: float
    created_at: Union[str, None, datetime] = None
    error: str = None
