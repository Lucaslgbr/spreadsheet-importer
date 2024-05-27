from app.core.ports.message_broker_port import MessageBrokerPort

class PublishService:
    def __init__(self, broker: MessageBrokerPort):
        self.broker = broker

    def publish_message(self, message: dict):
        self.broker.publish(message)