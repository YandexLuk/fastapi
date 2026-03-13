from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from infrastructure.sqlite.models.comment import Comment
from schemas.comment import CommentCreate, CommentUpdate

class CommentRepository:
    def __init__(self):
        self.model = Comment

    def get_by_id(self, session: Session, comment_id: int) -> Optional[Comment]:
        return session.get(self.model, comment_id)

    def get_all(self, session: Session) -> List[Comment]:
        return session.query(self.model).all()

    def create(self, session: Session, comment_data: CommentCreate) -> Comment:
        comment = self.model(
            text=comment_data.text,
            author_id=comment_data.author_id,
            post_id=comment_data.post_id,
            created_at=datetime.now()
        )
        session.add(comment)
        session.flush()
        return comment

    def update(self, session: Session, comment_id: int, comment_data: CommentUpdate) -> Optional[Comment]:
        comment = self.get_by_id(session, comment_id)
        if not comment:
            return None

        forbidden_fields = {'id', 'author_id', 'post_id', 'created_at'}
        update_data = comment_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if field not in forbidden_fields and hasattr(comment, field):
                if value is not None:
                    setattr(comment, field, value)

        return comment

    def delete(self, session: Session, comment_id: int) -> bool:
        comment = self.get_by_id(session, comment_id)
        if comment:
            session.delete(comment)
            return True
        return False