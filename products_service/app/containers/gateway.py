from dependency_injector import containers, providers
from app.infra.db import AsyncSessionLocal
from app.infra.redis import get_redis_client
from app.repositories.product_repo import ProductRepository
from app.use_cases.product import GetProductUseCase, UpdateProductUseCase, DeleteProductUseCase

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["app.api.product_router"])
    redis_client = providers.Singleton(get_redis_client)
    db_session_factory = providers.Object(AsyncSessionLocal)

    #Репозитории
    product_repo = providers.Factory(
        ProductRepository,
        session_factory=db_session_factory
    )

    #Юзкейсы (внедряем в них репозиторий и редиску)
    get_product_use_case = providers.Factory(
        GetProductUseCase,
        product_repo=product_repo,
        redis_client=redis_client
    )

    update_product_use_case = providers.Factory(
        UpdateProductUseCase, product_repo=product_repo, redis_client=redis_client
    )

    delete_product_use_case = providers.Factory(
        DeleteProductUseCase, product_repo=product_repo, redis_client=redis_client
    )