import enum
from sqlalchemy import ForeignKey, String, Integer, Float, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from orders_service.app.schemas.orders_schemas import OrderStatus
from orders_service.infra.database.db_config import Base

class GuitarType(str, enum.Enum):
    ELECTRIC = "электрогитара"
    ACOUSTIC = "акустическая гитара"
    CLASSICAL = "классическая гитара"
    BASS = "бас гитара"

class PickupConfig(str, enum.Enum):
    SSS = "SSS"
    HH = "HH"
    HSS = "HSS"
    HSH = "HSH"
    SS = "SS"
    P90 = "P90"
    PIEZO = "piezo"
    NONE = "none"

class OrderORM(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus), 
        default=OrderStatus.CREATED,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    items: Mapped[list["OrderItemORM"]] = relationship(back_populates="order", cascade="all, delete-orphan")

class OrderItemORM(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)

    sku: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    brand: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    type: Mapped[GuitarType] = mapped_column(SQLEnum(GuitarType), nullable=False)
    body_wood: Mapped[str] = mapped_column(String(50), nullable=False)
    neck_wood: Mapped[str] = mapped_column(String(50), nullable=False)
    fretboard_wood: Mapped[str] = mapped_column(String(50), nullable=False)
    fret_count: Mapped[int] = mapped_column(Integer, nullable=False)
    scale_length: Mapped[float] = mapped_column(Float, nullable=False)
    pickup_config: Mapped[PickupConfig] = mapped_column(SQLEnum(PickupConfig), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(512), nullable=True)

    order: Mapped["OrderORM"] = relationship(back_populates="items")