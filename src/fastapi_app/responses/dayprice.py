from datetime import datetime

from src.fastapi_app.responses.base import BaseResponse


class hourPrice(BaseResponse):
    hour: datetime
    totalprice: float
    spotprice: float
    isMax: bool
    isMin: bool


class DaypriceResponse(BaseResponse):
    qdate: datetime
    uuid: str
    prices: list[hourPrice]
