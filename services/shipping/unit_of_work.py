from repository.shipping.shipping_repository import ShippingRepository
from sqlalchemy.orm import sessionmaker
import db.engine as engine
from event_store.event_store import EventStore
from configs import RedisKeys
from schemas.shipping.shipping_schemas import ShipmentDto


class ShippingUnitOfWork:
    def __init__(self):
        self.Base = sessionmaker(autocommit=False, autoflush=False, bind=engine.engine)
        self.session = self.Base()
        self.repository = ShippingRepository(self.session)
        self.event_store = EventStore()
        self.event_mapper = {
            RedisKeys.ORDER_ALLOCATED.value: (ShipmentDto, self.create_shipment),
            RedisKeys.ORDER_DEALLOCATED.value: (ShipmentDto, self.cancel_shipment),
        }

    def get_line_order(self, ref):
        return self.repository.get_line_order(ref)

    def get_shipment_by_id(self, shipment_id: int):
        return self.repository.get_shipment_by_id(shipment_id)

    def create_shipment(self, shipment):
        self.repository.create_shipment(shipment)

    def decrease_line_order_qty(self, shipment, line_order):
        line_order.qty -= shipment.qty
        self.repository.update_line_order(line_order.order_ref, line_order.qty)

    def increase_line_order_qty(self, shipment, line_order):
        line_order.qty += shipment.qty
        self.repository.update_line_order(line_order.order_ref, line_order.qty)

    def create_order_lines(self):
        self.repository.create_order_lines()
        self.session.commit()

    def commit_transaction(self):
        self.session.commit()

    def check_event_store(self, key):
        shipment = self.event_store.subscribe_event(key)

        ProperSchema = self.event_mapper.get(key, None)[0]
        proper_action = self.event_mapper.get(key, None)[1]
        import pdb

        pdb.set_trace()
        if ProperSchema is None or proper_action is None:
            raise Exception
        proper_action(ProperSchema(**shipment))

    def cancel_shipment(self, shipment):
        line_order = self.get_line_order(shipment.order_ref)
        self.increase_line_order_qty(shipment, line_order)
        self.repository.update_shipment(shipment, [("status", shipment.status)])
