from pydantic import BaseModel


class ShipmentRequest(BaseModel):
    order_ref: str
    qty: str
