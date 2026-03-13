from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CommentBase(BaseModel):
    text: str = Field(..., max_length=10)

class CommentCreate(CommentBase):
    post_id: int
    author_id: int

class CommentUpdate(BaseModel):
    text: Optional[str] = None

class Comment(CommentBase):
    id: int
    author_id: int
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True