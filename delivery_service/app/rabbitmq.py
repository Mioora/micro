import traceback
from app.services.delivery_service import DeliveryService
from asyncio import AbstractEventLoop
from uuid import UUID
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage
from app.settings import settings


async def process_create_delivery(msg: IncomingMessage):
    try:
        print(msg.body.decode())
        DeliveryService().create_delivery(UUID(msg.body.decode()))
        await msg.ack()
    except:
        traceback.print_exc()


async def consume(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    order_created_queue = await channel.declare_queue("order_queue", durable=True)

    await order_created_queue.consume(process_create_delivery)
    print('Started RabbitMq consuming...')

    return connection
