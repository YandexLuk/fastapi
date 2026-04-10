from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.post_repository import PostRepository
from core.exceptions.database_exceptions import PostNotFoundError as DBPostNotFoundError
from core.exceptions.domain_exceptions import PostNotFoundError

class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> dict:
        try:
            with self._database.session() as session:
                deleted = self._repo.delete(session, post_id)
                return {"deleted": deleted}
        except DBPostNotFoundError as e:
            raise PostNotFoundError(f"id={post_id}") from e