from event_store.event_store import EventStore
from configs import RedisKeys
from domain.shipping.events import OrderAllocated, OrderDeallocated
from domain.shipping.value_objects import OrderLine

event_store = EventStore()


class Shipment:
    def __init__(self, order_ref, qty, status=None):
        self.order_ref = order_ref
        self.qty = qty
        self._allocation = []
        self.status = status

    def can_allocate(self, line: OrderLine):
        return self.order_ref == line.order_ref and self.qty <= line.qty

    def can_deallocate(self, line: OrderLine):
        return self.order_ref == line.order_ref

    def allocate(self, line: OrderLine):
        if line in self._allocation:
            raise Exception("")
        self._allocation.append(line)
        self.status = "Created"
        event_store.publish_event(
            RedisKeys.ORDER_ALLOCATED.value,
            OrderAllocated(
                order_ref=line.order_ref, qty=self.qty, status=self.status
            ).dict(),
        )

    def deallocate(self, line: OrderLine):
        self.status = "Cancelled"
        event_store.publish_event(
            RedisKeys.ORDER_DEALLOCATED.value,
            OrderDeallocated(
                order_ref=line.order_ref, qty=self.qty, status=self.status
            ).dict(),
        )
