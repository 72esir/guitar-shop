from dependency_injector import providers, containers
from broker.kafka.client.kafka_client import KafkaClient
from orders_service.app.repositories.orders_repo import OrdersRepository
from orders_service.app.use_cases.create_order_use_case import CreateOrderUseCase
from orders_service.config import settings
from orders_service.infra.database.db_config import Database
from orders_service.infra.kafka.producers.order_created_producer import OrderCreatedProducer

def create_session(db: Database):
    return db.get_session_factory()()

class Container(containers.DeclarativeContainer):

    config = providers.Object(settings)

    db = providers.Singleton(
        Database,
        db_url = config.provided.db_url
    )

    session = providers.Factory(
        create_session,
        db=db,
    )

    orders_repo = providers.Factory(
        OrdersRepository,
        session=session,
    )

    kafka_client = providers.Singleton(
        KafkaClient,
        config.provided.bootstrap_servers,
    )

    order_created_producer = providers.Factory(
        OrderCreatedProducer,
        kafka_client,
    )

    create_order_use_case = providers.Factory(
        CreateOrderUseCase,
        repo=orders_repo,
        producer=order_created_producer,
    )