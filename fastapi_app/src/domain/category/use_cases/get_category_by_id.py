from typing import Optional
from fastapi import HTTPException, status
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.category_repository import CategoryRepository
from schemas.category import Category


class GetCategoryByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> Optional[Category]:
        try:
            with self._database.session() as session:
                category = self._repo.get_by_id(session, category_id)
                if not category:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Категория с id {category_id} не найдена"
                    )
                return Category.model_validate(category)
        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при получении категории: {e}")
            raise