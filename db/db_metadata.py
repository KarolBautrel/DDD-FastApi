import logging
from sqlalchemy.orm import relationship, registry
from sqlalchemy import MetaData, Table, Column, String, Integer, ForeignKey
from domain.shipping.model import Shipment, OrderLine
from sqlalchemy import create_engine

mapper_registry = registry()

logger = logging.getLogger(__name__)


order_lines = Table(
    "order_lines",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("order_ref", String(255)),
    Column("qty", Integer, nullable=False),
)

shipments = Table(
    "shipments",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("order_ref", String, ForeignKey("order_lines.order_ref")),
    Column("qty", Integer, nullable=False),
)


def start_mapper():
    mapper_registry.map_imperatively(OrderLine, order_lines)
    mapper_registry.map_imperatively(Shipment, shipments)