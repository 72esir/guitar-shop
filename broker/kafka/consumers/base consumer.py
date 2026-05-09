from broker.kafka.client.kafka_client import KafkaClient

class BaseConsumer:

    topic: str
    group_id: str

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
                await self.process_message(message) 
                pass

        finally:
            await self.consumer.stop()

    async def process_message(self, message):
        raise NotImplementedError