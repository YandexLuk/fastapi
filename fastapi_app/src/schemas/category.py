from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    title: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True