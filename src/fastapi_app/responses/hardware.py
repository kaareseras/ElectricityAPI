from datetime import datetime
from typing import Union

from src.fastapi_app.responses.base import BaseResponse


class HardwareResponse(BaseResponse):
    id: int
    devicetype_id: int
    version: str
    name: str
    description: Union[str, None] = None
    created_at: datetime
    is_active: bool
