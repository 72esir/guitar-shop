from pydantic import BaseModel
from enum import Enum

from orders_service.app.schemas.order_items_schema import OrderItem

class OrderStatus(str, Enum):
    CREATED = "created"      
    PAID = "paid"            
    PROCESSING = "processing"
    CANCELLED = "cancelled"  

class OrderCreate(BaseModel):
    username: str
    items: list[OrderItem]
    status: OrderStatus = OrderStatus.CREATED

class Order(OrderCreate):
    id: int

class OrderUpdate(BaseModel):
    status: OrderStatus