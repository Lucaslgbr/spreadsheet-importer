import pika
import json
import os
from app.core.ports.message_broker_port import MessageBrokerPort

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'notifications')

class RabbitMQAdapter(MessageBrokerPort):
    def publish(self, message: dict):
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters(RABBITMQ_HOST, 5672, '/', credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )
        connection.close()