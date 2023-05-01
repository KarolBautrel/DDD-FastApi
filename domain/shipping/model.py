from dataclasses import dataclass


@dataclass()
class OrderLine:
    order_ref: str
    qty: int


class Shipment:
    def __init__(self, order_ref, qty):
        self.order_ref = order_ref
        self.qty = qty
        self._allocation = set()

    def can_allocate(self, line: OrderLine):
        self.order_ref == line.order_ref and self.qty <= line.qty

    def allocate(self, line: OrderLine):
        self._allocation.add(line)

    def deallocate(self, line: OrderLine):
        self._allocation.pop(line)
