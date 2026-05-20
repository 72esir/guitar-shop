from typing import Sequence, Optional
from sqlalchemy import select
from app.infra.model import Product

class ProductRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        async with self.session_factory() as session:
            query = select(Product).where(Product.id == product_id)
            result = await session.execute(query)
            return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[Product]:
        async with self.session_factory() as session:
            query = select(Product).offset(skip).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()

    async def create(self, product_data: dict) -> Product:
        async with self.session_factory() as session:
            db_product = Product(**product_data)
            session.add(db_product)
            await session.commit()
            await session.refresh(db_product)
            return db_product

    async def update(self, product_id: int, update_data: dict) -> Optional[Product]:
        async with self.session_factory() as session:
            db_product = await session.get(Product, product_id)
            if not db_product:
                return None

            for key, value in update_data.items():
                if hasattr(db_product, key):
                    setattr(db_product, key, value)

            session.add(db_product)
            await session.commit()
            await session.refresh(db_product)
            return db_product

    async def delete(self, product_id: int) -> bool:
        async with self.session_factory() as session:
            db_product = await session.get(Product, product_id)
            if not db_product:
                return False

            await session.delete(db_product)
            await session.commit()
            return True