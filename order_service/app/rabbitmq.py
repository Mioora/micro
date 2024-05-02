from uuid import UUID
from app.settings import settings
import pika


def send_queue_msg(body: UUID):
    connection = pika.BlockingConnection(pika.ConnectionParameters(settings.amqp_url, settings.amqp_port))
    channel = connection.channel()
    channel.queue_declare('order_queue', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='order_queue',
        body=str(body)
    )
    print("SEND")

    connection.close()
