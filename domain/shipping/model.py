from event_store.event_store import EventStore
from configs import RedisKeys
from domain.shipping.events import OrderAllocated, OrderDeallocated
from domain.shipping.value_objects import OrderLine, RamCube, GraphicsCard, Processor

event_store = EventStore()


class Computer:
    def __init__(self, ram_cube:RamCube, graphics_card:GraphicsCard, processor:Processor, backref:str):
        self.ram_cube = ram_cube
        self.graphics_card = graphics_card
        self.processor = processor
        self.backref = backref
        self.order_refs = [self.ram_cube.order_ref, self.graphics_card.order_ref, self.processor.order_ref]

    def change_part(self, part, line):
        part_change_map = {
            'RamCube':self.change_ram,
            'GraphicsCard': self.change_card,
            "Processor":self.change_processor
        }
        if self.able_to_change(part,line):
            proper_part_method = part_change_map.get(part.__class__.__name__, None)
            if proper_part_method is None:
                raise Exception
            proper_part_method(part)
    def able_to_change(self, part, line):
        return part.order_ref not in self.order_refs and line.qty > 0
    def change_ram(self, ram_cube):
            self.ram_cube = ram_cube
            # Send event

    def change_card(self, graphics_card):
            self.graphics_card = graphics_card
            # Send event
    def change_processor(self, processor):
            self.processor = processor
            # Send event



class Shipment:
    def __init__(self, order_ref, qty, computer:Computer, status=None):
        self.order_ref = order_ref
        self.qty = qty
        self.computer = computer
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
