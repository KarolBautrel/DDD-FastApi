from services.shipping.unit_of_work import ShippingUnitOfWork
from domain.shipping.model import Shipment, OrderLine
from configs import RedisKeys


class ShippingService:
    def __init__(self):
        self.uow = ShippingUnitOfWork()

    def create_order_lines(self):
        """
        This is only for testing purposes
        """
        self.uow.create_order_lines()

    def create_new_shipment(self, shipment: Shipment):
        import pdb

        pdb.set_trace()
        self.map_shipment(shipment)
        line_order = self.uow.get_line_order(self.shipment.order_ref)
        if line_order is None:
            raise Exception
        if self.shipment.can_allocate(line_order):
            self.shipment.allocate(line_order)
            self.uow.check_event_store(RedisKeys.ORDER_ALLOCATED.value)
            self.uow.decrease_line_order_qty(self.shipment, line_order)
            self.uow.commit_transaction()

    def map_shipment(self, shipment: Shipment) -> None:
        self.shipment = Shipment(order_ref=shipment.order_ref, qty=shipment.qty)
