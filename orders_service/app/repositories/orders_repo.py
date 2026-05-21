from typing import Sequence
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from orders_service.app.schemas.order_items_schema import OrderItem
from orders_service.app.schemas.orders_schemas import OrderCreate, OrderUpdate
from orders_service.infra.database.models import OrderItemORM, OrderORM


class OrdersRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_order(self, order_data: OrderCreate) -> int:
        new_order = OrderORM(username=order_data.username)

        for item in order_data.items:
            new_order.items.append(
                OrderItemORM(
                    product_id=item.product_id,
                    sku=item.sku,
                    title=item.title,
                    brand=item.brand,
                    price=item.price,
                    quantity=item.quantity,
                    type=item.type,
                    body_wood=item.body_wood,
                    neck_wood=item.neck_wood,
                    fretboard_wood=item.fretboard_wood,
                    fret_count=item.fret_count,
                    scale_length=item.scale_length,
                    pickup_config=item.pickup_config,
                    image_url=item.image_url
                )
            )

        self.session.add(new_order)
        await self.session.commit()
        await self.session.refresh(new_order)

        return new_order.id

    async def delete_order(self, order_id: int) -> bool:
        order = await self.get_order(order_id)
        if order:
            await self.session.delete(order)
            await self.session.commit()
            return True
        return False

    async def update_order(self, order_id: int, payload: OrderUpdate):
        order = await self.get_order(order_id)
        if not order:
            return None

        if payload.status:
            order.status = payload.status

        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def get_order(self, order_id: int) -> OrderORM | None:
        query = select(OrderORM).where(OrderORM.id == order_id).options(selectinload(OrderORM.items))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_orders(self) -> Sequence[OrderORM]:
        query = select(OrderORM).options(selectinload(OrderORM.items))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def add_item_to_order(self, item_data: OrderItem, order_id: int) -> int:
        new_item = OrderItemORM(
            order_id=order_id,
            product_id=item_data.product_id,
            sku=item_data.sku,
            title=item_data.title,
            brand=item_data.brand,
            price=item_data.price,
            quantity=item_data.quantity,
            type=item_data.type,
            body_wood=item_data.body_wood,
            neck_wood=item_data.neck_wood,
            fretboard_wood=item_data.fretboard_wood,
            fret_count=item_data.fret_count,
            scale_length=item_data.scale_length,
            pickup_config=item_data.pickup_config,
            image_url=item_data.image_url
        )
        self.session.add(new_item)
        await self.session.commit()
        await self.session.refresh(new_item)
        return new_item.id

    async def remove_order_item(self, item_id: int) -> bool:
        query = select(OrderItemORM).where(OrderItemORM.id == item_id)
        result = await self.session.execute(query)
        item = result.scalar_one_or_none()

        if item:
            await self.session.delete(item)
            await self.session.commit()
            return True
        return False