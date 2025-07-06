from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from settings import mongo_cfg, logger


def connect_to_mongodb():
    try:
        client = AsyncIOMotorClient(mongo_cfg.url())
        logger.info("Successful connect to MongoDB")
        return AsyncIOMotorDatabase(client, mongo_cfg.DB)
    except Exception as e:
        logger.info(f"Error with connection to MongoDB: {e}")
        return None
    
def connect_to_test_mongodb():
    try:
        client = AsyncIOMotorClient(mongo_cfg.url())
        logger.info("Successful connect to test MongoDB")
        return AsyncIOMotorDatabase(client, mongo_cfg.TEST_DB)
    except Exception as e:
        logger.info(f"Error with connection to test MongoDB: {e}")
        return None