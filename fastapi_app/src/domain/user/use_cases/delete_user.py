from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.user_repository import UserRepository
from core.exceptions.database_exceptions import UserNotFoundError as DBUserNotFoundError
from core.exceptions.domain_exceptions import UserNotFoundError

class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> dict:
        try:
            with self._database.session() as session:
                deleted = self._repo.delete(session, user_id)
                return {"deleted": deleted}
        except DBUserNotFoundError as e:
            raise UserNotFoundError(f"id={user_id}") from e