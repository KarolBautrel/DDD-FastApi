from pydantic import BaseModel


class ShipmentRequest(BaseModel):
    order_ref: str
    qty: int


class ShipmentDto(BaseModel):
    order_ref: str
    qty: int
    status: str
