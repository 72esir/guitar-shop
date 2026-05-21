from orders_service.app.schemas.orders_schemas import OrderUpdate
from orders_service.app.repositories.orders_repo import OrdersRepository
from fastapi import HTTPException

class UpdateOrderUseCase:
    def __init__(
        self, 
        repo: OrdersRepository
    ) -> None:
        self.repo = repo
    
    async def execute(self, order_id: int, update_data: OrderUpdate):
        order = await self.repo.update_order(order_id, update_data)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
