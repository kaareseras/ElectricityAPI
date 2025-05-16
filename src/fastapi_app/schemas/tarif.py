from datetime import datetime

from pydantic import BaseModel


class AddTarifRequest(BaseModel):
    valid_from: datetime
    valid_to: datetime
    nettarif: float
    systemtarif: float
    includingVAT: bool
