from pydantic import BaseModel
from typing import Optional

from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(..., max_length=150)
    email: str = Field(..., max_length=254)
    password: str = Field(..., min_length=8, max_length=64)

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True