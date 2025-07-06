from typing import Union

from src.fastapi_app.schemas.base import BaseSchema


class DeviceTypeSchema(BaseSchema):
    name: str
    description: Union[str, None] = None
