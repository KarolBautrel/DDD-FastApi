from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship


SQLALCHEMY_DATABASE_URL = "sqlite:///database.db"  # Sqlite for local fast deployment
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:qazXS567!!];ACfrw@192.168.1.47:5432/trading_broker"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)

Base = declarative_base()


class StockProduct(Base):
    __tablename__ = "order_lines"

    id = Column(Integer, primary_key=True)
    order_ref = Column(String(255), nullable=False)
    qty = Column(Integer, nullable=False)


class Shipments(Base):
    __tablename__ = "Shipments"

    id = Column(Integer, primary_key=True)
    order_ref = Column(Integer, ForeignKey("order_lines.order_ref"))
    qty = Column(Integer, nullable=False)


Base.metadata.create_all(bind=engine)
