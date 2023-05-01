from repository.shipping.shipping_repository import ShippingRepository
from sqlalchemy.orm import sessionmaker
import db.engine as engine


class ShippingUnitOfWork:
    def __init__(self):
        self.Base = sessionmaker(autocommit=False, autoflush=False, bind=engine.engine)
        self.session = self.Base()
        self.repository = ShippingRepository(self.session)

    def get_line_order(self, ref):
        return self.repository.get_line_order(ref)

    def create_shipment(self, shipment):
        self.repository.create_shipment(shipment)
        self.session.commit()

    def decrease_line_order_qty(self, shipment, line_order):
        line_order.qty -= shipment.qty
        self.repository.update_line_order(line_order.ref, line_order.qty)
        self.session.commit()

    def create_order_lines(self):
        self.repository.create_order_lines()
        self.session.commit()
