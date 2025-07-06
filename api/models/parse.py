from pydantic import BaseModel, Field
from typing import Annotated, Optional

class ParseModel(BaseModel):
    text: Annotated[str, Field(max_length=50)]
    salary: Optional[int] = None
    city: Annotated[str, Field(max_length=50)] | None = None
    
class ParseResponseModel(BaseModel):
    task_id: str