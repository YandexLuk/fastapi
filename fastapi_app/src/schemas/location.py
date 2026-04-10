from pydantic import BaseModel, Field, validator
from typing import Optional

class LocationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=256)

    @validator('name')
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Название локации не может быть пустым')
        return v

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=256)

    @validator('name')
    def name_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Название локации не может быть пустым')
        return v

class Location(LocationBase):
    id: int

    class Config:
        from_attributes = True