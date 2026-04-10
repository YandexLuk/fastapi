from slugify import slugify
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.category_repository import CategoryRepository
from schemas.category import Category, CategoryUpdate
from core.exceptions.database_exceptions import (
    CategoryNotFoundError as DBCategoryNotFoundError,
    CategoryAlreadyExistsError as DBCategoryAlreadyExistsError
)
from core.exceptions.domain_exceptions import (
    CategoryNotFoundError,
    CategoryAlreadyExistsError
)

class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int, category_data: CategoryUpdate) -> Category:
        try:
            with self._database.session() as session:
                try:
                    existing_category = self._repo.get_by_id(session, category_id)
                except DBCategoryNotFoundError:
                    raise CategoryNotFoundError(f"id={category_id}")

                # Если меняется title, slug изменится автоматически в репозитории при update
                if category_data.title is not None and category_data.title != existing_category.title:
                    new_slug = slugify(category_data.title)
                    same_slug = self._repo.get_by_slug(session, new_slug)
                    if same_slug and same_slug.id != category_id:
                        raise CategoryAlreadyExistsError("slug", new_slug)

                updated_category = self._repo.update(session, category_id, category_data)
                return Category.model_validate(updated_category)
        except DBCategoryAlreadyExistsError as e:
            raise CategoryAlreadyExistsError("slug", "unknown") from e