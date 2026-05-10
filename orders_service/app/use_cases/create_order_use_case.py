from orders_service.app.repositories.orders_repo import OrdersRepository
from orders_service.app.schemas.orders_schemas import OrderCreate
from orders_service.infra.kafka.producers.order_created_producer import OrderCreatedProducer
from event_contracts.orders.order_created_event import OrderCreatedEvent


class CreateOrderUseCase:

    def __init__(
        self,
        repo: OrdersRepository,
        producer: OrderCreatedProducer,
    ) -> None:
        self. repo = repo
        self.producer = producer

    async def execute(self, order: OrderCreate):
        order_id: int = await self.repo.create_order(order)

        event = OrderCreatedEvent(
            username=order.username,
            order_id=order_id
        )

        await self.producer.publish(event)

        return order_id