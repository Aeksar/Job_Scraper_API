import aio_pika
from aio_pika.abc import AbstractConnection
from settings import rabbit_cfg, logger


TTL = 60000

async def connect_to_rabbit():
    global rabbit_cfg
    url = rabbit_cfg.url()
    connection =  await aio_pika.connect_robust(url)
    logger.info("Successful connect to rabbit")
    return connection


async def setup_rabbit(connection: AbstractConnection):
    global TTL, rabbit_cfg
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    args = {"x-message-ttl" : TTL}
    await channel.declare_queue(rabbit_cfg.PRODUCE_QUEUE, arguments=args)
    callback_queue = await channel.declare_queue(exclusive=True, auto_delete=True)
    return channel, callback_queue