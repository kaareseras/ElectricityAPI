from src.fastapi_app.schemas.base import BaseSchema


class AddDeviceRequest(BaseSchema):
    uuid: str


class UpdateDeviceRequest(BaseSchema):
    uuid: str
    name: str | None
    chargeowner_id: int | None
    PriceArea: str | None
    Config: str | None
