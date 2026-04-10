from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.user_repository import UserRepository
from schemas.user import User
from core.exceptions.database_exceptions import UserNotFoundError as DBUserNotFoundError
from core.exceptions.domain_exceptions import UserNotFoundError

class GetUserByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> User:
        try:
            with self._database.session() as session:
                user = self._repo.get_by_id(session, user_id)
                return User.model_validate(user)
        except DBUserNotFoundError as e:
            raise UserNotFoundError(f"id={user_id}") from e