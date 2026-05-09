import asyncio
import uvicorn
import logging
from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from notifications_service.containers import container
from notifications_service.containers.container import Container

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    container = Container()
    container.config.kafka_bootstrap_servers.from_value(
        os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    )

    consumer = container.order_created_consumer()

    kafka_task = asyncio.create_task(consumer.start())
    logger.info("Kafka Consumer started")

    yield

    logger.info("Shutting down Kafka Consumer")
    kafka_task.cancel()
    try:
        await kafka_task
    except asyncio.CancelledError:
        logger.info("Kafka Consumer task cancelled.")


app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "notifications"}


if __name__ == "__main__":
    uvicorn.run("notifications_service.main:app", host="0.0.0.0", port=8001, reload=True)