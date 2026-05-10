from pydantic import BaseModel

class OrderItemCreate(BaseModel):
    title: str
    price: int
    quantity: int = 1
    # TODO Данич добей

class OrderItem(OrderItemCreate):
    id: int
