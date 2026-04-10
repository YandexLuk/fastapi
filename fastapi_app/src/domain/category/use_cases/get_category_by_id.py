from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.category_repository import CategoryRepository
from schemas.category import Category
from core.exceptions.database_exceptions import CategoryNotFoundError as DBCategoryNotFoundError
from core.exceptions.domain_exceptions import CategoryNotFoundError

class GetCategoryByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> Category:
        try:
            with self._database.session() as session:
                category = self._repo.get_by_id(session, category_id)
                return Category.model_validate(category)
        except DBCategoryNotFoundError as e:
            raise CategoryNotFoundError(f"id={category_id}") from e