from src.fastapi_app.schemas.base import BaseSchema


class AddChargeownerRequest(BaseSchema):
    glnnumber: str
    compagny: str
    chargetype: str
    chargetypecode: str


class UpdateChargeownerRequest(AddChargeownerRequest):
    id: int
    is_active: bool
