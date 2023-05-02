from domain.shipping.model import Shipment
from domain.shipping.value_objects import OrderLine
from schemas.shipping.shipping_schemas import ShipmentDto
from typing import List, Optional


class ShippingRepository:
    def __init__(self, session):
        self.session = session

    def get_shipments(self) -> List[Shipment]:
        self.session.query(Shipment).all()

    def get_shipment_by_ref(self, ref) -> Optional[Shipment]:
        return self.session.query(Shipment).filter(Shipment.order_ref == ref).first()

    def get_shipment_by_id(self, id) -> Optional[Shipment]:
        return self.session.query(Shipment).filter(Shipment.id == id).first()

    def get_line_order(self, ref) -> Optional[OrderLine]:
        return self.session.query(OrderLine).filter(OrderLine.order_ref == ref).first()

    def create_shipment(self, shipment: ShipmentDto) -> Shipment:
        import pdb

        pdb.set_trace()
        self.session.add(
            Shipment(
                order_ref=shipment.order_ref, qty=shipment.qty, status=shipment.status
            )
        )

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

    def update_shipment(self, shipment, shipment_attrs):
        shipment_instance_db = (
            self.session.query(Shipment)
            .filter(Shipment.order_ref == shipment.order_ref)
            .first()
        )
        import pdb

        pdb.set_trace()
        if shipment_instance_db is None:
            raise Exception("There is no record like this in db")
        for data in shipment_attrs:
            import pdb

            pdb.set_trace()
            setattr(shipment_instance_db, data[0], data[1])
