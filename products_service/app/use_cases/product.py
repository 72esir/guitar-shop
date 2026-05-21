import json
from typing import Optional, List
from redis.asyncio import Redis
from app.repositories.product_repo import ProductRepository
from app.schemas.product_DTOs import ProductResponse

from celery import Celery
from config import settings

class GetRecommendationsUseCase:
    def __init__(self, product_repo: ProductRepository, redis_recs: Redis):
        self.product_repo = product_repo
        self.redis_recs = redis_recs

    async def execute(self, product_id: int) -> List[ProductResponse]:
        recs_data = await self.redis_recs.get(f"recs:product:{product_id}")
        if not recs_data:
            return []
        
        product_ids = json.loads(recs_data)
        products = []
        for p_id in product_ids:
            product = await self.product_repo.get_by_id(p_id)
            if product:
                products.append(ProductResponse.model_validate(product))
        return products

class TriggerRecommendationUpdateUseCase:
    def __init__(self):
        self.celery_app = Celery("recs_worker", broker=settings.celery_broker_url)

    async def execute(self):
        self.celery_app.send_task("recs_worker.tasks.calculate_recommendations")
        return {"status": "Calculation task sent to worker"}

class GetProductUseCase:
    def __init__(self, product_repo: ProductRepository, redis_client: Redis):
        self.product_repo = product_repo
        self.redis = redis_client

    async def execute(self, product_id: int) -> Optional[dict]:
        cache_key = f"product:{product_id}"

        #кэш
        cached = await self.redis.get(cache_key)
        if cached:
            return json.loads(cached)

        #если кэша нет — запрашиваем репозиторий
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            return None

        product_data = ProductResponse.model_validate(product).model_dump()

        #пишем в кэш (время жизни — 10 минут)
        await self.redis.set(cache_key, json.dumps(product_data), ex=600)
        return product_data

class UpdateProductUseCase:
    def __init__(self, product_repo: ProductRepository, redis_client: Redis):
        self.product_repo = product_repo
        self.redis = redis_client

    async def execute(self, product_id: int, update_data: dict) -> Optional[dict]:
        #обновляем в бд
        product = await self.product_repo.update(product_id, update_data)
        if not product:
            return None

        #дропаем кэш
        cache_key = f"product:{product_id}"
        await self.redis.delete(cache_key)

        return ProductResponse.model_validate(product).model_dump()

class DeleteProductUseCase:
    def __init__(self, product_repo: ProductRepository, redis_client: Redis):
        self.product_repo = product_repo
        self.redis = redis_client

    async def execute(self, product_id: int) -> bool:
        #удаляем в бд
        success = await self.product_repo.delete(product_id)
        if not success:
            return False

        #дропаем кэш
        cache_key = f"product:{product_id}"
        await self.redis.delete(cache_key)
        return True