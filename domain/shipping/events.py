from pydantic import BaseModel


class OrderAllocated(BaseModel):
    order_ref: str
    qty: int
    status: str


class OrderDeallocated(BaseModel):
    order_ref: str
    qty: int
    status: str
