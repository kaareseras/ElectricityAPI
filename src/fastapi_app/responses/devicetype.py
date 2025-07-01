from datetime import datetime
from typing import Union

from src.fastapi_app.responses.base import BaseResponse


class DeviceTypeResponse(BaseResponse):
    id: int
    name: str
    hw_version: Union[str, None] = None
    sw_version: Union[str, None] = None
    sw_date: Union[str, None, datetime] = None
