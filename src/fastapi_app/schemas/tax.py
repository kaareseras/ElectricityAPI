from datetime import datetime

from src.fastapi_app.schemas.base import BaseSchema


class AddTaxRequest(BaseSchema):
    valid_from: datetime
    valid_to: datetime
    taxammount: float
    includingVAT: bool
