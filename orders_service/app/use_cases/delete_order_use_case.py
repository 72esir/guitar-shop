from orders_service.app.repositories.orders_repo import OrdersRepository
from fastapi import HTTPException

class DeleteOrderUseCase:
    def __init__(
        self, 
        repo: OrdersRepository
    ) -> None:
        self.repo = repo
    
    async def execute(self, order_id: int) -> bool:
        success = await self.repo.delete_order(order_id)
        if not success:
            raise HTTPException(status_code=404, detail="Order not found")
        return success
