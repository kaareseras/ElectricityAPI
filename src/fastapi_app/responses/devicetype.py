from datetime import datetime
from typing import Union

from src.fastapi_app.responses.base import BaseResponse


class DeviceTypeResponse(BaseResponse):
    id: int
    name: str
    description: Union[str, None] = None
    created_at: Union[str, None, datetime] = None


class DeviceTypeListResponse(BaseResponse):
    id: int
    name: str
    created_at: Union[str, None, datetime] = None
    fw_version: Union[str, None] = None
    fw_date: Union[datetime, None] = None
    hw_version: Union[str, None] = None
