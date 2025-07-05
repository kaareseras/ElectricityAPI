from datetime import datetime
from typing import Union

from src.fastapi_app.responses.base import BaseResponse


class FirmwareResponse(BaseResponse):
    id: int
    devicetype_id: int
    version: str
    filename: str
    repo_url: Union[str, None] = None
    is_active: bool
    created_at: Union[str, datetime]
