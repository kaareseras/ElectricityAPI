from pydantic import BaseModel


class AddChargeownerRequest(BaseModel):
    glnnumber: str
    company: str
    chargetype: str
    chargetypecode: str


class UpdateChargeownerRequest(AddChargeownerRequest):
    id: int
    is_active: bool
