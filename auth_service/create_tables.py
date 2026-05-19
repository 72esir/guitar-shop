import asyncio

from app.database.database import engine
from app.database.database import Base

from app.models.user import User


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(create_tables())