from repository.shipping.shipping_repository import ShippingRepository


class ShippingService:
    def __init__(self):
        self.repository = ShippingRepository()

    def create_order_lines(self):
        self.repository.create_order_lines()
