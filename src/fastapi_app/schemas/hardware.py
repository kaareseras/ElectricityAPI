from typing import Optional

from src.fastapi_app.schemas.base import BaseSchema


class HardwareSchema(BaseSchema):
    devicetype_id: int
    version: str
    name: str
    description: Optional[str] = None
    is_active: bool
