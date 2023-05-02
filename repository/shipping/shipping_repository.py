from domain.shipping.model import Shipment, OrderLine
from schemas.shipping.shipping_schemas import ShipmentRequest
from typing import List, Optional


class ShippingRepository:
    def __init__(self, session):
        self.session = session

    def get_shipments(self) -> List[Shipment]:
        self.session.query(Shipment).all()

    def get_shipment(self, ref) -> Optional[Shipment]:
        return self.session.query(Shipment).filter(Shipment.order_ref == ref).first()

    def get_line_order(self, ref) -> Optional[OrderLine]:
        return self.session.query(OrderLine).filter(OrderLine.order_ref == ref).first()

    def create_shipment(self, shipment: ShipmentRequest) -> Shipment:
        self.session.add(Shipment(order_ref=shipment.order_ref, qty=shipment.qty))

    def update_line_order(self, ref, qty):
        line_order = (
            self.session.query(OrderLine).filter(OrderLine.order_ref == ref).first()
        )
        line_order.qty = qty

    def create_order_lines(self):
        """
        This method is only for mocking orderlines
        """
        self.session.add(OrderLine(order_ref="NIKE-AIR-MAX", qty=50))
        self.session.add(OrderLine(order_ref="ADIDAS-SUPERSTAR", qty=30))
        self.session.add(OrderLine(order_ref="PUMA-SUPER", qty=20))
        self.session.add(OrderLine(order_ref="REEBOK-CLASS", qty=25))
        self.session.add(OrderLine(order_ref="NIKE-SPORT", qty=30))
