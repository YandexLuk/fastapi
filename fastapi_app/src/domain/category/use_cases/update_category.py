from typing import Optional
from fastapi import HTTPException, status
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.category_repository import CategoryRepository
from schemas.category import CategoryUpdate, Category


class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int, category_data: CategoryUpdate) -> Optional[Category]:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_id(session, category_id)
                if not existing:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Категория с id {category_id} не найдена"
                    )

                if category_data.slug is not None:
                    slug_exists = self._repo.get_by_slug(session, category_data.slug)
                    if slug_exists and slug_exists.id != category_id:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Категория со slug '{category_data.slug}' уже существует"
                        )

                updated = self._repo.update(session, category_id, category_data)
                return Category.model_validate(updated)
        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при обновлении категории: {e}")
            raise