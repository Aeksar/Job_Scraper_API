from fastapi import APIRouter, status, HTTPException
import json

from api.models.parse import ParseModel
from services.mongo import TaskCollection, mongo_client
from services.rabbit import produce_message, get_conection

parse_rout = APIRouter()

@parse_rout.post("/parse")
async def start_parsing(params: ParseModel):
    params = params.model_dump()
    task_col = TaskCollection(mongo_client)
    task_id = await task_col.add(params)
    rabbit_conn = await get_conection()
    await produce_message(str(task_id), rabbit_conn)
    await task_col.update_status(task_id, "processing")
    return {"task_id": str(task_id)}
    
@parse_rout.get("/task/{task_id}")
async def check_parse_task(task_id: str):
    task_col = TaskCollection(mongo_client)
    status = await task_col.get_status(task_id)
    if not status:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if status == "completed":
        return await task_col.get(task_id)
    return {"status": status, "message": "wait bro"}