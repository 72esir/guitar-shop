from broker.kafka.producers.base_producer import BaseProducer

class OrderCreatedProducer(BaseProducer):

    topic = "order.created"
