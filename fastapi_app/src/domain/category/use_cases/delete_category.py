from fastapi import HTTPException, status
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.category_repository import CategoryRepository


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> dict:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_id(session, category_id)
                if not existing:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Категория с id {category_id} не найдена"
                    )

                deleted = self._repo.delete(session, category_id)
                return {"deleted": deleted}
        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при удалении категории: {e}")
            raise