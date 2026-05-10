from sqlalchemy import ForeignKey, String, Integer, Float, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from orders_service.app.schemas.orders_schemas import OrderStatus
from orders_service.infra.database.db_config import Base

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
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    order: Mapped["OrderORM"] = relationship(back_populates="items")