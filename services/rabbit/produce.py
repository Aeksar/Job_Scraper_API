from aio_pika.abc import AbstractConnection
import aio_pika
import json


from services.rabbit.conf import setup_rabbit
from settings import logger, RabbitConfig
    
    
async def produce_message(task_id: str, connection: AbstractConnection):
    ch, callback_queue  = await setup_rabbit(connection)
    payload = {
        "title": "hh",
        "task_id": task_id,
    }
    message = aio_pika.Message(
        body=json.dumps(payload).encode(),
        reply_to=callback_queue.name,
    )
    await ch.default_exchange.publish(
        message=message,
        routing_key=RabbitConfig().PRODUCE_QUEUE,
    )
    logger.info(f"Send message to MQ -> {payload}")