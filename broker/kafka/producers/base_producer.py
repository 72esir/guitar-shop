from broker.kafka.client.kafka_client import KafkaClient

from pydantic import BaseModel

class BaseProducer:

    topic: str

    def __init__(self, kafka_client: KafkaClient) -> None:
        self.kafka_client = kafka_client

    async def publish(self, event: BaseModel):
        value = event.model_dump_json().encode('utf-8')

        await self.kafka_client.producer.send_and_wait(
            self.topic,
            value
        )