from src.fastapi_app.schemas.base import BaseSchema


class AddDeviceRequest(BaseSchema):
    uuid: str
    devicetype_id: int


class UpdateDeviceRequest(BaseSchema):
    uuid: str
    name: str | None
    chargeowner_id: int | None
    price_area: str | None
    is_electric_heated: bool
    config: str | None
    devicetype_id: int
    retail_markup: float | None = None


class AdoptDeviceRequest(BaseSchema):
    uuid: str
    name: str | None = None
    chargeowner_id: int
    price_area: str
    is_electric_heated: bool
    devicetype_id: int
    retail_markup: float | None = None
