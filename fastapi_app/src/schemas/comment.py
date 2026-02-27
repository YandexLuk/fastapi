from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .user import User  # для вложенного объекта

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    post_id: int
    author_id: int

class CommentUpdate(BaseModel):
    text: Optional[str] = None

class Comment(CommentBase):
    id: int
    author: User
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True