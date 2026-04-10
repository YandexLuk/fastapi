from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from infrastructure.sqlite.models.post import Post
from schemas.post import PostCreate, PostUpdate
from core.exceptions.database_exceptions import (
    DatabaseError, PostNotFoundError
)

class PostRepository:
    def __init__(self):
        self.model = Post

    def get_by_id(self, session: Session, post_id: int) -> Post:
        try:
            post = session.get(self.model, post_id)
            if post is None:
                raise PostNotFoundError(f"Post with id {post_id} not found")
            return post
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error: {e}")

    def get_all(self, session: Session) -> List[Post]:
        try:
            return session.query(self.model).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error: {e}")

    def create(self, session: Session, post_data: PostCreate) -> Post:
        try:
            post = self.model(
                title=post_data.title,
                text=post_data.text,
                pub_date=post_data.pub_date,
                author_id=post_data.author_id,
                category_id=post_data.category_id,
                location_id=post_data.location_id,
                is_published=True,
                created_at=datetime.now(),
                image=None
            )
            session.add(post)
            session.flush()
            return post
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error while creating post: {e}")

    def update(self, session: Session, post_id: int, post_data: PostUpdate) -> Post:
        try:
            post = self.get_by_id(session, post_id)
            update_data = post_data.model_dump(exclude_unset=True)
            forbidden_fields = {'id', 'author_id', 'created_at'}
            for field, value in update_data.items():
                if field not in forbidden_fields and value is not None:
                    setattr(post, field, value)
            session.flush()
            return post
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error while updating post: {e}")

    def delete(self, session: Session, post_id: int) -> bool:
        try:
            post = self.get_by_id(session, post_id)
            session.delete(post)
            return True
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error while deleting post: {e}")