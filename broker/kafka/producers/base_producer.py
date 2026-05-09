from broker.kafka.client.kafka_client import KafkaClient


class BaseProducer:

    topic: str

    def __init__(self, kafka_client: KafkaClient) -> None:
        self.kafka_client = kafka_client

    async def publish(self, value: bytes):
        await self.kafka_client.producer.send_and_wait(
            self.topic,
            value
        )