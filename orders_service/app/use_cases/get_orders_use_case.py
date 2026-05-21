from orders_service.app.repositories.orders_repo import OrdersRepository
from orders_service.app.schemas.orders_schemas import Order
from orders_service.app.schemas.order_items_schema import OrderItem

class GetOrdersUseCase:
    def __init__(self, repo: OrdersRepository) -> None:
        self.repo = repo

    async def execute(self):
        orders_orm = await self.repo.get_orders()

        orders_dto = []
        for order in orders_orm:
            items = [OrderItem.model_validate(item) for item in order.items]
            orders_dto.append(Order(
                username=order.username,
                status=order.status,
                items=items,
                id=order.id
            ))

        return orders_dto