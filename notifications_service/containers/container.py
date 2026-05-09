from dependency_injector import containers, providers

from broker.kafka.client.kafka_client import KafkaClient
from notifications_service.app.use_cases.send_message_use_case import SendMessageUseCase
from notifications_service.infra.kafka.consumers.order_created_consumer import OrderCreatedConsumer

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    kafka_client = providers.Singleton(
        KafkaClient,
        bootstrap_servers = config.kafka_bootstrap_servers,
    )

    send_message_use_case = providers.Factory(
        SendMessageUseCase,
    )

    order_created_consumer = providers.Factory(
        OrderCreatedConsumer,
        kafka_client = kafka_client,
        send_message_use_case = send_message_use_case
    )