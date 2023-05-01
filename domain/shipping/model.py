from event_store.event_store import EventStore
from configs import RedisKeys
from domain.shipping.events import OrderAllocated

event_store = EventStore()


class OrderLine:
    def __init__(self, order_ref, qty):
        self.order_ref = order_ref
        self.qty = qty


class Shipment:
    def __init__(self, order_ref, qty):
        self.order_ref = order_ref
        self.qty = qty
        self._allocation = []

    def can_allocate(self, line: OrderLine):
        return self.order_ref == line.order_ref and self.qty <= line.qty

    def allocate(self, line: OrderLine):
        if line in self._allocation:
            raise Exception("")
        self._allocation.append(line)
        event_store.publish_event(
            RedisKeys.ORDER_ALLOCATED.value,
            OrderAllocated(order_ref=self.order_ref, qty=self.qty).dict(),
        )
        """
        Will be replaced with event send, for now we 
        weill stick to the unit of work.
        """

    def deallocate(self, line: OrderLine):
        if line in self._allocation:
            self._allocation.pop(line)
