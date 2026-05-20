from pydantic import BaseModel, Field

class OrderItemCreate(BaseModel):
    product_id: int = Field(..., description="ID купленной гитары из сервиса продуктов")
    sku: str = Field(..., description="Артикул товара на момент покупки")
    title: str = Field(..., description="Название гитары на момент оформления заказа")
    price: float = Field(..., description="Цена за штуку")
    quantity: int = Field(1, ge=1, description="Количество товара в заказе, минимум 1")

class OrderItem(OrderItemCreate):
    id: int
    model_config = {"from_attributes": True}