from pydantic import BaseModel

class OrderCreatedEvent(BaseModel):
    username: str
    order_id: int