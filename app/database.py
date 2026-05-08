import redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Поменяйте здесь бд на нашу
# postgresql://пользователь:пароль@хост:порт/имя_базы
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/product_db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

redis_pool = redis.ConnectionPool.from_url("redis://localhost:6379", decode_responses=True)

async def get_redis():
    yield redis.Redis(connection_pool=redis_pool)