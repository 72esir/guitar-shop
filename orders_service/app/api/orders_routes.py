from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide

from orders_service.app.containers.container import Container
from orders_service.app.use_cases.create_order_use_case import CreateOrderUseCase
from orders_service.app.schemas.orders_schemas import OrderCreate

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", status_code=201)
@inject
async def create_order(
    order_data: OrderCreate,
    use_case: CreateOrderUseCase = Depends(Provide[Container.create_order_use_case])
):
    try:
        order_id = await use_case.execute(order_data)
        return {"order_id": order_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))