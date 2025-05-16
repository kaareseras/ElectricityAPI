from pydantic import BaseModel


class AddChargeownerRequest(BaseModel):
    name: str
    glnnumber: str
    company: str
    type: str
    chargetype: str


class UpdateChargeownerRequest(AddChargeownerRequest):
    id: int
    is_active: bool
