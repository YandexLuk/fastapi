from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class CommentBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)

    @validator('text')
    def text_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Текст комментария не может быть пустым')
        return v

class CommentCreate(CommentBase):
    post_id: int
    author_id: int

class CommentUpdate(BaseModel):
    text: Optional[str] = Field(None, min_length=1, max_length=1000)

    @validator('text')
    def text_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Текст комментария не может быть пустым')
        return v

class Comment(CommentBase):
    id: int
    author_id: int
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True