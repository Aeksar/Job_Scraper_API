import aio_pika
from aio_pika.abc import AbstractConnection
from settings import RabbitConfig, logger


TTL = 60000

cfg = RabbitConfig()

async def get_conection():
    global cfg
    url = cfg.url()
    connection =  await aio_pika.connect_robust(url)
    logger.info("Successful connect to rabbit")
    return connection


async def setup_rabbit(connection: AbstractConnection):
    global TTL, cfg
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    args = {"x-message-ttl" : TTL}
    await channel.declare_queue(cfg.PRODUCE_QUEUE, arguments=args)
    callback_queue = await channel.declare_queue(exclusive=True, auto_delete=True)
    return channel, callback_queue