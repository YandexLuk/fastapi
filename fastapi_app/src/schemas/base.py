from pydantic import BaseModel
from datetime import datetime

class BaseWithId(BaseModel):
    id: int

class BaseWithDates(BaseModel):
    created_at: datetime
    updated_at: datetime | None = None