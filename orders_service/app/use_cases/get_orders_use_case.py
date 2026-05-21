from orders_service.app.repositories.orders_repo import OrdersRepository


class GetOrdersUseCase:
    def __init__(self, repo: OrdersRepository) -> None:
        self.repo = repo

    async def execute(self):
        orders = await self.repo.get_orders()
        return orders