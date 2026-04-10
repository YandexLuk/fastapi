from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from infrastructure.sqlite.models.comment import Comment
from schemas.comment import CommentCreate, CommentUpdate
from core.exceptions.database_exceptions import (
    DatabaseError, CommentNotFoundError
)

class CommentRepository:
    def __init__(self):
        self.model = Comment

    def get_by_id(self, session: Session, comment_id: int) -> Comment:
        try:
            comment = session.get(self.model, comment_id)
            if comment is None:
                raise CommentNotFoundError(f"Comment with id {comment_id} not found")
            return comment
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error: {e}")

    def get_all(self, session: Session) -> List[Comment]:
        try:
            return session.query(self.model).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error: {e}")

    def create(self, session: Session, comment_data: CommentCreate) -> Comment:
        try:
            comment = self.model(
                text=comment_data.text,
                author_id=comment_data.author_id,
                post_id=comment_data.post_id,
                created_at=datetime.now()
            )
            session.add(comment)
            session.flush()
            return comment
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error while creating comment: {e}")

    def update(self, session: Session, comment_id: int, comment_data: CommentUpdate) -> Comment:
        try:
            comment = self.get_by_id(session, comment_id)
            update_data = comment_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(comment, field) and value is not None:
                    setattr(comment, field, value)
            session.flush()
            return comment
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error while updating comment: {e}")

    def delete(self, session: Session, comment_id: int) -> bool:
        try:
            comment = self.get_by_id(session, comment_id)
            session.delete(comment)
            return True
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error while deleting comment: {e}")