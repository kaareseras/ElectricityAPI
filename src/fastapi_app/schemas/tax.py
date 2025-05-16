from datetime import datetime

from pydantic import BaseModel


class AddTaxRequest(BaseModel):
    valid_from: datetime
    valid_to: datetime
    taxammount: float
    includingVAT: bool
