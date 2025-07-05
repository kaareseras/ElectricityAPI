from datetime import date
from typing import Optional

from src.fastapi_app.schemas.base import BaseSchema


class FirmwareSchema(BaseSchema):
    devicetype_id: int
    version: str
    filename: str
    repo_url: Optional[str] = None
    is_active: bool
    created_at: date
