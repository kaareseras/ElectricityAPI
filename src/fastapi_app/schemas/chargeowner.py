from pydantic import BaseModel


class AddChargeownerRequest(BaseModel):
    glnnumber: str
    compagny: str
    chargetype: str
    chargetypecode: str


class UpdateChargeownerRequest(AddChargeownerRequest):
    id: int
    is_active: bool
