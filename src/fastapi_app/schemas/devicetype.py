from datetime import date
from typing import Optional

from src.fastapi_app.schemas.base import BaseSchema


class DeviceTypeSchema(BaseSchema):
    name: str
    hw_version: Optional[str] = None
    sw_version: Optional[str] = None
    sw_date: Optional[date] = None
