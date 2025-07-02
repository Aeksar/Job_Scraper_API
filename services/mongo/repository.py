from motor.motor_asyncio import  AsyncIOMotorClient
from pymongo import ReturnDocument
from bson.objectid import ObjectId
from bson.datetime_ms import DatetimeMS
from datetime import datetime
from settings import logger


class HhCollection:
    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.db = self.client["job_name"]
        self.collection = self.db["hh"]
        
    async def find_by_ids(self, ids: list[str]) -> list[dict]:
        valid_ids = []
        for id in ids:
            valid_ids.append(ObjectId(id))
        res = await self.collection.find({"_id": {"$in": valid_ids}}, {"_id": 0}).to_list()
        return res
    

class TaskCollection:
    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.db = self.client["job_name"]
        self.collection = self.db["search_result"]
        self.jobs_col = HhCollection(self.client)    

    async def add(self, params: dict) -> ObjectId:
        res = await self.collection.insert_one({
            "status": "pending",
            "parameters": params,
            "created_at": DatetimeMS(datetime.now())
        })
        return res.inserted_id
    
    async def get(self, task_id: str) -> dict:
        document = await  self.collection.find_one({"_id": ObjectId(task_id)})
        job_ids = document["jobs"]
        return await self.jobs_col.find_by_ids(job_ids)
    
    async def update_status(self, task_id: str, status: str,):
        filter = {"_id": ObjectId(task_id)}
        update = {"$set": {"status": status}}
        await self.collection.update_one(filter, update)
        
    async def get_status(self, task_id: str):
        doc = await self.collection.find_one({"_id": ObjectId(task_id)})
        return doc["status"]