from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from infrastructure.sqlite.models.category import Category
from schemas.category import CategoryCreate, CategoryUpdate

class CategoryRepository:
    def __init__(self):
        self.model = Category

    def get_by_id(self, session: Session, category_id: int) -> Optional[Category]:
        return session.get(self.model, category_id)

    def get_all(self, session: Session) -> List[Category]:
        return session.query(self.model).all()

    def create(self, session: Session, category_data: CategoryCreate) -> Category:
        """Создать категорию"""
        from slugify import slugify
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

    def update(self, session: Session, category_id: int, category_data: CategoryUpdate) -> Optional[Category]:
        category = self.get_by_id(session, category_id)
        if not category:
            return None

        forbidden_fields = {'id', 'slug', 'created_at'}
        update_data = category_data.model_dump(exclude_unset=True)

        if 'title' in update_data:
            from slugify import slugify
            update_data['slug'] = slugify(update_data['title'])

        for field, value in update_data.items():
            if field not in forbidden_fields and hasattr(category, field):
                if value is not None:
                    setattr(category, field, value)

        return category

    def delete(self, session: Session, category_id: int) -> bool:
        category = self.get_by_id(session, category_id)
        if category:
            session.delete(category)
            return True
        return False