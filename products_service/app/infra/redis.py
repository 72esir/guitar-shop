import redis.asyncio as redis
from config import settings

redis_pool = redis.ConnectionPool.from_url(settings.redis_url, decode_responses=True)
recs_pool = redis.ConnectionPool.from_url(f"{settings.redis_url}/{settings.redis_db_recs}", decode_responses=True)

def get_redis_client():
    return redis.Redis(connection_pool=redis_pool)

def get_recs_redis_client():
    return redis.Redis(connection_pool=recs_pool)