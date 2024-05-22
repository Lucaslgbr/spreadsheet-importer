import pika
import os
import json

RABBITMQ_HOST = 'amqp://guest:guest@rabbitmq:5672'
RABBITMQ_QUEUE = 'notifications'


def publish_to_rabbitmq(message: dict):
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
    print(RABBITMQ_HOST, RABBITMQ_QUEUE)
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