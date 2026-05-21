from fastapi import HTTPException
from orders_service.app.schemas.order_items_schema import OrderItem
from orders_service.app.schemas.orders_schemas import Order
from orders_service.app.repositories.orders_repo import OrdersRepository

class GetOrderUseCase:
    def __init__(
        self, 
        repo: OrdersRepository
    ) -> None:
        self.repo = repo
    
    async def execute(self, order_id: int):
        order = await self.repo.get_order(order_id)
        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")

        items = [OrderItem.model_validate(item) for item in order.items]

        order_dto = Order(
            username=order.username,
            status=order.status,
            items=items,
            id=order.id
        )

        return order_dto