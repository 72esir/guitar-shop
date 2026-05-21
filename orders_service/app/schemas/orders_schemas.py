from pydantic import BaseModel
from enum import Enum

from orders_service.app.schemas.order_items_schema import OrderItem, OrderItemCreate

class OrderStatus(str, Enum):
    CREATED = "created"      
    PAID = "paid"            
    PROCESSING = "processing"
    CANCELLED = "cancelled"  

class OrderCreate(BaseModel):
    username: str
    items: list[OrderItemCreate]
    status: OrderStatus = OrderStatus.CREATED

class Order(OrderCreate):
    id: int
    items: list[OrderItem]

class OrderUpdate(BaseModel):
    status: OrderStatus