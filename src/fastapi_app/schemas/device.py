from pydantic import BaseModel


class AddDeviceRequest(BaseModel):
    uuid: str


class UpdateDeviceRequest(BaseModel):
    uuid: str
    name: str | None
    chargeowner_id: int | None
    PriceArea: str | None
    Config: str | None
