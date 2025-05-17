from datetime import datetime
from typing import Union

from src.fastapi_app.responses.base import BaseResponse


class DeviceResponse(BaseResponse):
    uuid: str
    name: Union[str, None] = None
    user_id: Union[int, None] = None
    chargeowner_id: Union[int, None] = None
    PriceArea: Union[str, None] = None
    Config: Union[str, None] = None
    last_activity: Union[str, None, datetime] = None
    created_at: Union[str, None, datetime] = None
