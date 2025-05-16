from datetime import datetime
from typing import Union

from src.fastapi_app.responses.base import BaseResponse


class ChargeResponse(BaseResponse):
    id: int
    chargeowner_id: int
    charge_type: str
    charge_type_code: str
    note: str
    description: str
    valid_from: Union[str, None, datetime] = None
    valid_to: Union[str, None, datetime] = None
    price1: float
    price2: float
    price3: float
    price4: float
    price5: float
    price6: float
    price7: float
    price8: float
    price9: float
    price10: float
    price11: float
    price12: float
    price13: float
    price14: float
    price15: float
    price16: float
    price17: float
    price18: float
    price19: float
    price20: float
    price21: float
    price22: float
    price23: float
    price24: float
    created_at: Union[str, None, datetime] = None
