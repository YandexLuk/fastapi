from pydantic import BaseModel, Field, validator
from typing import Optional

class CategoryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=256)
    description: Optional[str] = ""

    @validator('title')
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Название категории не может быть пустым')
        return v

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=256)
    description: Optional[str] = None

    @validator('title')
    def title_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Название категории не может быть пустым')
        return v

class Category(CategoryBase):
    id: int
    slug: str

    class Config:
        from_attributes = True