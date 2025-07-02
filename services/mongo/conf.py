from motor.motor_asyncio import AsyncIOMotorClient

from settings import MongoConfig, logger

cfg = MongoConfig()

def connect_to_mongodb():
    try:
        client = AsyncIOMotorClient(
            f"mongodb://{cfg.USER}:{cfg.PASSWORD}@{cfg.HOST}:{cfg.PORT}/"
        )
        logger.info("Successful connect to MongoDB")
        return client
    except Exception as e:
        logger.info(f"Error with connection to MongoDB: {e}")
        return None
    
mongo_client = connect_to_mongodb()