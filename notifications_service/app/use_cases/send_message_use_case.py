from event_contracts.orders.order_created_event import OrderCreatedEvent
import logging

logger = logging.getLogger(__name__)

class SendMessageUseCase:

    async def execute(self, event: OrderCreatedEvent):
        logger.info(
            f"[NOTIFICATION SENT] "
            f"username={event.username} "
            f"message=Order {event.order_id} created! "
        )