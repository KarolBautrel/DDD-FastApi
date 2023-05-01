from pydantic import BaseModel


class OrderAllocated(BaseModel):
    order_ref: str
    qty: int
