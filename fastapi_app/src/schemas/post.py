from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .user import User
from .category import Category
from .location import Location
from .comment import Comment

class PostBase(BaseModel):
    title: str
    text: str
    pub_date: datetime

class PostCreate(PostBase):
    author_id: int
    category_id: Optional[int] = None
    location_id: Optional[int] = None

class PostUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    pub_date: Optional[datetime] = None
    category_id: Optional[int] = None
    location_id: Optional[int] = None

class Post(PostBase):
    id: int
    author: User
    category: Optional[Category] = None
    location: Optional[Location] = None
    comments: List[Comment] = []

    class Config:
        from_attributes = True