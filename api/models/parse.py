from pydantic import BaseModel, Field
from typing import Annotated, Optional

class ParseModel(BaseModel):
    position: Annotated[str, Field(max_length=50)]
    salary: Optional[int] = None
    city: Annotated[str, Field(max_length=20)] | None = None
    