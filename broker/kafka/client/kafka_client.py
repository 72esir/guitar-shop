from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

class KafkaClient:
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self.producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers
        ) 

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    def create_consumer(self, topic: str, group_id: str):
        return AIOKafkaConsumer(
            topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=group_id,
        )