from datetime import datetime
from typing import Optional

from src.fastapi_app.schemas.base import BaseSchema


class AddChargeRequest(BaseSchema):
    chargeowner_id: int
    charge_type: str
    charge_type_code: str
    note: str
    description: str
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
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
