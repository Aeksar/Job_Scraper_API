from pydantic import BaseModel,HttpUrl
from typing import Optional
from enum import Enum

class StatusEnum(str, Enum):
    COMPLETED = "completed"
    PENDING = "pending"
    PROCESSING = "processing"

class JobModel(BaseModel):
    company: str
    job_name: str
    city: str
    link: HttpUrl
    salary: Optional[str] = None
    
class ListJobModel(BaseModel):
    status: StatusEnum
    result: list[JobModel]
    
class UncompletedModel(BaseModel):
    status: StatusEnum
    message: str