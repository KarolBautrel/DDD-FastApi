from fastapi import APIRouter
from domain.shipping.service import ShippingService

router = APIRouter(prefix="/shipping", tags=["shipping"])
ShippingServiceImpl = ShippingService()


@router.post("/")
def create_shipping():
    pass


@router.get("/")
def get_shippings():
    pass


@router.get("/order_lines")
def create_order_lines_test():
    ShippingServiceImpl.create_order_lines()
