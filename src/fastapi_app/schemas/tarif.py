from datetime import datetime

from src.fastapi_app.schemas.base import BaseSchema


class AddTarifRequest(BaseSchema):
    valid_from: datetime
    valid_to: datetime
    nettarif: float
    systemtarif: float
    includingVAT: bool
