from services.shipping.unit_of_work import ShippingUnitOfWork
from domain.shipping.model import Shipment
from domain.shipping.value_objects import OrderLine
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
        shipment_domain_model = self.map_shipment(shipment)
        line_order = self.uow.get_line_order(shipment_domain_model.order_ref)
        if line_order is None:
            raise Exception
        if shipment_domain_model.can_allocate(line_order):
            shipment_domain_model.allocate(line_order)
            self.uow.check_event_store(RedisKeys.ORDER_ALLOCATED.value)
            self.uow.decrease_line_order_qty(shipment_domain_model, line_order)
            self.uow.commit_transaction()

    def cancel_shipment(self, shipment_id: int):
        shipment = self.uow.get_shipment_by_id(shipment_id)
        import pdb

        pdb.set_trace()
        if shipment.status == "Cancelled":
            raise Exception("Status is already canceled")
        shipment_domain_model = self.map_shipment(shipment)

        line_order = self.uow.get_line_order(shipment_domain_model.order_ref)

        if line_order is None:
            raise Exception
        if shipment_domain_model.can_deallocate(line_order):
            shipment_domain_model.deallocate(line_order)
            self.uow.check_event_store(RedisKeys.ORDER_DEALLOCATED.value)
            self.uow.commit_transaction()

    def map_shipment(self, shipment: Shipment) -> None:
        return Shipment(order_ref=shipment.order_ref, qty=shipment.qty)
