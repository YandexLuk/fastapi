from fastapi import HTTPException, status
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.category_repository import CategoryRepository
from schemas.category import Category, CategoryCreate

class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_data: CategoryCreate) -> Category:
        try:
            with self._database.session() as session:
                existing_slug = self._repo.get_by_slug(session, category_data.slug)
                if existing_slug:
                    raise HTTPException(...)
                new_category = self._repo.create(session, category_data)
                return Category.model_validate(new_category)
        except HTTPException:
            raise
        except Exception as e:
            print(...)
            raise