from fastapi import APIRouter, status
from services.shipping.service import ShippingService
from schemas.shipping.shipping_schemas import ShipmentRequest

router = APIRouter(prefix="/shipping", tags=["shipping"])
ShippingServiceImpl = ShippingService()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_shipment(request: ShipmentRequest):
    ShippingServiceImpl.create_new_shipment(request)


@router.patch("/{id}/cancel", status_code=status.HTTP_200_OK)
def cancel_shipment(shipment_id: int):
    import pdb

    pdb.set_trace()
    ShippingServiceImpl.cancel_shipment(shipment_id)


@router.get("/")
def get_shipments():
    pass


@router.get("/order_lines")
def create_order_lines_test():
    ShippingServiceImpl.create_order_lines()
