from pydantic import BaseModel


class ComputerCreateRequest(BaseModel):
    order_ref: str
    qty: int


class ComputerDTO(BaseModel):
    order_ref: str
    qty: int
    status: str


class PartChangeDTO(BaseModel):
    computer_backref: str
    part_backref: str
    part_name: str
