from repository.shipping.shipping_repository import ShippingRepository
from sqlalchemy.orm import sessionmaker
import db.engine as engine
from event_store.event_store import EventStore
from configs import RedisKeys
from schemas.shipping.shipping_schemas import ShipmentRequest


class ShippingUnitOfWork:
    def __init__(self):
        self.Base = sessionmaker(autocommit=False, autoflush=False, bind=engine.engine)
        self.session = self.Base()
        self.repository = ShippingRepository(self.session)
        self.event_store = EventStore()
        self.event_mapper = {RedisKeys.ORDER_ALLOCATED.value: ShipmentRequest}

    def get_line_order(self, ref):
        return self.repository.get_line_order(ref)

    def create_shipment(self, shipment):
        self.repository.create_shipment(shipment)

    def decrease_line_order_qty(self, shipment, line_order):
        line_order.qty -= shipment.qty
        self.repository.update_line_order(line_order.order_ref, line_order.qty)

    def create_order_lines(self):
        self.repository.create_order_lines()

    def commit_transaction(self):
        self.session.commit()

    def check_event_store(self, key):
        shipment = self.event_store.subscribe_event(key)
        ProperSchema = self.event_mapper.get(key, None)
        if ProperSchema is None:
            raise Exception

        self.create_shipment(ProperSchema(**shipment))
