from fastapi import APIRouter, status, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Annotated

from api.models.parse import ParseModel
from services.mongo import TaskCollection, connect_to_mongodb
from services.rabbit import produce_message, get_conection

parse_rout = APIRouter()

@parse_rout.post("/parse")
async def start_parsing(
    params: ParseModel,
    mongo_client: Annotated[AsyncIOMotorClient, Depends(connect_to_mongodb)]
):
    params = params.model_dump()
    task_col = TaskCollection(mongo_client)
    task_id = await task_col.add(params)
    rabbit_conn = await get_conection()
    await produce_message(str(task_id), rabbit_conn)
    await task_col.update_status(task_id, "processing")
    return {"task_id": str(task_id)}
    
    
@parse_rout.get("/task/{task_id}")
async def check_parse_task(
    task_id: str,
    mongo_client: Annotated[AsyncIOMotorClient, Depends(connect_to_mongodb)]
):
    task_col = TaskCollection(mongo_client)
    task_status = await task_col.get_status(task_id)
    if not task_status:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found task")
    if task_status == "completed":
        return await task_col.get_jobs(task_id)
    return {"status": task_status, "message": "wait bro"}