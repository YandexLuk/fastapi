from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.category_repository import CategoryRepository
from schemas.category import Category, CategoryCreate
from core.exceptions.database_exceptions import CategoryAlreadyExistsError as DBCategoryAlreadyExistsError
from core.exceptions.domain_exceptions import CategoryAlreadyExistsError

class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_data: CategoryCreate) -> Category:
        try:
            with self._database.session() as session:
                new_category = self._repo.create(session, category_data)
                return Category.model_validate(new_category)
        except DBCategoryAlreadyExistsError as e:
            raise CategoryAlreadyExistsError(e.field, e.value) from e