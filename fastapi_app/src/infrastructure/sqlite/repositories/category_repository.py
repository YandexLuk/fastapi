from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from slugify import slugify
from infrastructure.sqlite.models.category import Category
from schemas.category import CategoryCreate, CategoryUpdate
from core.exceptions.database_exceptions import (
    DatabaseError, CategoryNotFoundError, CategoryAlreadyExistsError
)

class CategoryRepository:
    def __init__(self):
        self.model = Category

    def get_by_id(self, session: Session, category_id: int) -> Category:
        try:
            category = session.get(self.model, category_id)
            if category is None:
                raise CategoryNotFoundError(f"Category with id {category_id} not found")
            return category
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error: {e}")

    def get_by_slug(self, session: Session, slug: str) -> Optional[Category]:
        try:
            return session.query(self.model).filter(self.model.slug == slug).first()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error: {e}")

    def get_all(self, session: Session) -> List[Category]:
        try:
            return session.query(self.model).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error: {e}")

    def create(self, session: Session, category_data: CategoryCreate) -> Category:
        try:
            slug = slugify(category_data.title)
            category = self.model(
                title=category_data.title,
                description=category_data.description or "",
                slug=slug,
                is_published=True,
                created_at=datetime.now()
            )
            session.add(category)
            session.flush()
            return category
        except IntegrityError as e:
            if "slug" in str(e.orig):
                raise CategoryAlreadyExistsError("slug", slug)
            raise DatabaseError(f"Integrity error: {e}")
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error: {e}")

    def update(self, session: Session, category_id: int, category_data: CategoryUpdate) -> Category:
        try:
            category = self.get_by_id(session, category_id)
            update_data = category_data.model_dump(exclude_unset=True)
            if 'title' in update_data:
                update_data['slug'] = slugify(update_data['title'])
            forbidden_fields = {'id', 'created_at'}
            for field, value in update_data.items():
                if field not in forbidden_fields and value is not None:
                    setattr(category, field, value)
            session.flush()
            return category
        except IntegrityError as e:
            if "slug" in str(e.orig):
                raise CategoryAlreadyExistsError("Category with this slug already exists")
            raise DatabaseError(f"Integrity error: {e}")
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error: {e}")

    def delete(self, session: Session, category_id: int) -> bool:
        try:
            category = self.get_by_id(session, category_id)
            session.delete(category)
            return True
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error: {e}")