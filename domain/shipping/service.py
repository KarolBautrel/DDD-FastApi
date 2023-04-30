from repository.shipping.shipping_repository import ShippingRepository
from domain.shipping.model import Shipment, OrderLine


class ShippingService:
    def __init__(self):
        self.repository = ShippingRepository()

    def create_order_lines(self):
        self.repository.create_order_lines()

    def create_new_shipment(self, shipment: Shipment):
        self.map_shipment(shipment)
        line_order = self.repository.get_line_order(self.shipment.order_ref)
        if line_order is None:
            raise Exception
        if self.shipment.can_allocate(line_order):
            self.shipment.allocate(line_order)
            self.repository.create_shipment(self.shipment)
            self.decrease_line_order_qty(self.shipment, line_order)

    def map_shipment(self, shipment: Shipment) -> None:
        self.shipment = Shipment(order_ref=shipment.order_ref, qty=shipment.qty)

    def decrease_line_order_qty(self, shipment, line_order):
        line_order.qty -= shipment.qty
        self.repository.update_line_order(line_order.ref, line_order.qty)

    def get_order_line(self):
        self.repository.get_line_order()
