from sqlalchemy.orm import sessionmaker
import db.engine as engine
from domain.shipping.model import Shipment, OrderLine
from schemas.shipping.shipping_schemas import ShipmentRequest
from typing import List


class ShippingRepository:
    def __init__(self):
        self.Base = sessionmaker(autocommit=False, autoflush=False, bind=engine.engine)
        self.session = self.Base()

    def map_shipment(self, shipment: Shipment) -> None:
        self.shipment = Shipment(order_ref=shipment.order_ref, qty=shipment.qty)

    def get(self) -> List[Shipment]:
        self.session.query(Shipment).all()

    def create_shipment(self, shipment: ShipmentRequest) -> Shipment:
        self.map_shipment(shipment)
        line_order = (
            self.session.query(OrderLine)
            .filter(OrderLine.order_ref == self.shipment.order_ref)
            .first()
        )
        if line_order is None:
            raise Exception
        if self.shipment.can_allocate(line_order):
            self.session.add(
                Shipment(order_ref=self.shipment.order_ref, qty=self.shipment.qty)
            )
            self.session.commit()
            return self.shipment

    def create_order_lines(self):
        """
        This method is only for mocking orderlines
        """
        self.session.add(OrderLine(order_ref="NIKE-AIR-MAX", qty=50))
        self.session.add(OrderLine(order_ref="ADIDAS-SUPERSTAR", qty=30))
        self.session.add(OrderLine(order_ref="PUMA-SUPER", qty=20))
        self.session.add(OrderLine(order_ref="REEBOK-CLASS", qty=25))
        self.session.add(OrderLine(order_ref="NIKE-SPORT", qty=30))
        self.session.commit()
