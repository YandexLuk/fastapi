from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=256)
    text: str = Field(..., min_length=1)
    pub_date: datetime

    @validator('title')
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Заголовок поста не может быть пустым')
        return v

    @validator('text')
    def text_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Содержание поста не может быть пустым')
        return v

class PostCreate(PostBase):
    author_id: int
    category_id: Optional[int] = None
    location_id: Optional[int] = None

class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=256)
    text: Optional[str] = Field(None, min_length=1)
    pub_date: Optional[datetime] = None
    category_id: Optional[int] = None
    location_id: Optional[int] = None

    @validator('title')
    def title_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Заголовок поста не может быть пустым')
        return v

    @validator('text')
    def text_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Содержание поста не может быть пустым')
        return v

class Post(PostBase):
    id: int
    author_id: int
    category_id: Optional[int] = None
    location_id: Optional[int] = None

    class Config:
        from_attributes = True