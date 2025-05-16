from datetime import datetime
from typing import Union

from src.fastapi_app.responses.base import BaseResponse


class TaxResponse(BaseResponse):
    id: int
    valid_from: Union[str, None, datetime] = None
    valid_to: Union[str, None, datetime] = None
    taxammount: float
    includingVAT: bool
    created_at: Union[str, None, datetime] = None
