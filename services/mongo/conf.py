from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from settings import MongoConfig, logger

cfg = MongoConfig()

def connect_to_mongodb():
    try:
        client = AsyncIOMotorClient(
            f"mongodb://{cfg.USER}:{cfg.PASSWORD}@{cfg.HOST}:{cfg.PORT}/"
        )
        logger.info("Successful connect to MongoDB")
        return AsyncIOMotorDatabase(client, cfg.DB)
    except Exception as e:
        logger.info(f"Error with connection to MongoDB: {e}")
        return None
    
def connect_to_test_mongodb():
    try:
        client = AsyncIOMotorClient(
            f"mongodb://{cfg.USER}:{cfg.PASSWORD}@{cfg.HOST}:{cfg.PORT}/"
        )
        logger.info("Successful connect to test MongoDB")
        return AsyncIOMotorDatabase(client, cfg.TEST_DB)
    except Exception as e:
        logger.info(f"Error with connection to test MongoDB: {e}")
        return None