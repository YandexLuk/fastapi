from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.category_repository import CategoryRepository
from core.exceptions.database_exceptions import CategoryNotFoundError as DBCategoryNotFoundError
from core.exceptions.domain_exceptions import CategoryNotFoundError

class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> dict:
        try:
            with self._database.session() as session:
                deleted = self._repo.delete(session, category_id)
                return {"deleted": deleted}
        except DBCategoryNotFoundError as e:
            raise CategoryNotFoundError(f"id={category_id}") from e