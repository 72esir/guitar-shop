from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.containers.gateway import Container
from app.api.product_router import router as product_router
from app.infra.db import engine
from app.infra.model import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

def create_app() -> FastAPI:
    container = Container()
    app = FastAPI(title="Clean Products Service", lifespan=lifespan)
    app.container = container
    app.include_router(product_router)

    return app

app = create_app()