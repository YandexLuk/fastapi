from typing import List
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.category_repository import CategoryRepository
from schemas.category import Category

class GetCategoriesUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self) -> List[Category]:
        with self._database.session() as session:
            categories = self._repo.get_all(session)
            return [Category.model_validate(c) for c in categories]