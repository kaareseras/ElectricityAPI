from datetime import datetime
from typing import Union

from src.fastapi_app.responses.base import BaseResponse


class ChargeownerResponse(BaseResponse):
    id: int
    name: str
    glnnumber: str
    company: str
    type: str
    chargetype: str
    is_active: bool
    created_at: Union[str, None, datetime] = None
    updated_at: Union[str, None, datetime] = None
    error: str = None


class ChargeownerListResponse(BaseResponse):
    id: int
    name: str
    glnnumber: str
    company: str
    type: str
    chargetype: str
    is_active: bool
