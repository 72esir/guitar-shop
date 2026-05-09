import json
from typing import Generic, TypeVar, Type
from pydantic import BaseModel
from broker.kafka.client.kafka_client import KafkaClient

T = TypeVar("T", bound=BaseModel)

class BaseConsumer(Generic[T]):

    topic: str
    group_id: str
    schema_class: Type[T]

    def __init__(self, kafka_client: KafkaClient) -> None:
        self.kafka_client = kafka_client
        self.consumer = kafka_client.create_consumer(
            topic=self.topic,
            group_id=self.group_id
        )

    async def start(self):
        await self.consumer.start()

        try:
            async for message in self.consumer:
                if message.value is None:
                    continue
                try: 
                    data = json.loads(message.value.decode('utf-8'))
                    event = self.schema_class(**data)
                    await self.process_message(event) 
                except Exception as e:
                    print(f"Error parsing message: {e}")

        finally:
            await self.consumer.stop()

    async def process_message(self, event: T):
        raise NotImplementedError