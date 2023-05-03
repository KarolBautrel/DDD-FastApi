class OrderLine:
    def __init__(self, order_ref, qty):
        self.order_ref = order_ref
        self.qty = qty



class RamCube:
    def __init__(self, size, qty):
        self.size = size
        self.order_ref = 'RAM-CUBE'
        self.qty = qty
class GraphicsCard:
    def __init__(self,size, brand, order_ref, qty):
        self.size = size
        self.brand = brand
        self.order_ref = order_ref
        self.qty = qty
class Processor:
    def __init__(self,size,brand,order_ref, qty):
        self.size = size
        self.brand = brand
        self.order_ref = order_ref
        self.qty = qty

