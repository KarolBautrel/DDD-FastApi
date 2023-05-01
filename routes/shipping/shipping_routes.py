from fastapi import APIRouter, status
from services.shipping.service import ShippingService
from schemas.shipping.shipping_schemas import ShipmentRequest

router = APIRouter(prefix="/shipping", tags=["shipping"])
ShippingServiceImpl = ShippingService()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_shipping(request: ShipmentRequest):
    ShippingServiceImpl.create_new_shipment(request)


@router.get("/")
def get_shippings():
    pass


@router.get("/order_lines")
def create_order_lines_test():
    ShippingServiceImpl.create_order_lines()
