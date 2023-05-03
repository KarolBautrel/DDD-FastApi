import logging
from sqlalchemy.orm import relationship, registry
from sqlalchemy import MetaData, Table, Column, String, Integer, ForeignKey
from domain.shipping.model import Shipment
from domain.shipping.value_objects import OrderLine, RamCube, GraphicsCard, Processor
from sqlalchemy import create_engine

mapper_registry = registry()

logger = logging.getLogger(__name__)
SQLALCHEMY_DATABASE_URL = "sqlite:///database.db"  # Sqlite for local fast deployment

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)

order_lines = Table(
    "order_lines",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("order_ref", String(255)),
    Column("qty", Integer, nullable=False),
)
ram_cubes = Table(
    'ram_cubes',
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("order_ref", String(255)),
    Column("qty", Integer, nullable=False),
    Column("size", String, nullable=False),

)
graph_cards = Table(
    'graph_cards',
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("order_ref", String(255)),
    Column("qty", Integer, nullable=False),
    Column("brand", String, nullable=False),
    Column("size", String, nullable=False),

)
processors = Table(
    'processors',
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("order_ref", String(255)),
    Column("qty", Integer, nullable=False),
    Column("size", String, nullable=False),
    Column("brand", String, nullable=False),

)

computer = Table(
    'computers',
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("ram_cube", String, ForeignKey("ram_cubes.order_ref")),
    Column("processor", String, ForeignKey("processors.order_ref")),
    Column("graph_card", String, ForeignKey("graph_cards.order_ref")),

    Column("backref", String, ),

)



shipments = Table(
    "shipments",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("order_ref", String, ForeignKey("order_lines.order_ref")),
    Column('computer', String, ForeignKey('computers.backref')),
    Column("qty", Integer, nullable=False),
    Column("status", String, nullable=False),
)


def start_mapper():
    mapper_registry.map_imperatively(OrderLine, order_lines)
    mapper_registry.map_imperatively(Shipment, shipments)
    mapper_registry.map_imperatively(RamCube, ram_cubes)
    mapper_registry.map_imperatively(GraphicsCard, graph_cards)
    mapper_registry.map_imperatively(Processor, processors)


mapper_registry.metadata.create_all(engine)
