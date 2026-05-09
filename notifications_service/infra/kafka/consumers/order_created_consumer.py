from broker.kafka.consumers.base_consumer import BaseConsumer
from broker.kafka.client.kafka_client import KafkaClient
from event_contracts.orders.order_created_event import OrderCreatedEvent
from notifications_service.app.use_cases.send_message_use_case import SendMessageUseCase

class OrderCreatedConsumer(BaseConsumer):

    topic = "order.created"
    group_id = "order-service"
    schema_class = OrderCreatedEvent

    def __init__(
        self, 
        kafka_client: KafkaClient,
        send_message_use_case: SendMessageUseCase, 
        ) -> None:
        super().__init__(kafka_client)

        self.send_message_use_case = send_message_use_case

    async def process_message(self, event: OrderCreatedEvent):

        await self.send_message_use_case.execute(event)

