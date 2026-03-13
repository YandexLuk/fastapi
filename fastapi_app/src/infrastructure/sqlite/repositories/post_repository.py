from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from infrastructure.sqlite.models.post import Post
from schemas.post import PostCreate, PostUpdate

class PostRepository:
    def __init__(self):
        self.model = Post

    def get_by_id(self, session: Session, post_id: int) -> Optional[Post]:
        """Получить пост по ID"""
        return session.get(self.model, post_id)

    def get_all(self, session: Session) -> List[Post]:
        """Получить все посты"""
        return session.query(self.model).all()

    def create(self, session: Session, post_data: PostCreate) -> Post:
        """Создать новый пост"""
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

    def update(self, session: Session, post_id: int, post_data: PostUpdate) -> Optional[Post]:
        """Обновить пост (частичное обновление)"""
        post = self.get_by_id(session, post_id)
        if not post:
            return None

        forbidden_fields = {'id', 'author_id', 'created_at'}

        update_data = post_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field not in forbidden_fields and hasattr(post, field):
                if value is not None:
                    setattr(post, field, value)

        return post

    def delete(self, session: Session, post_id: int) -> bool:
        """Удалить пост по ID"""
        post = self.get_by_id(session, post_id)
        if post:
            session.delete(post)
            return True
        return False