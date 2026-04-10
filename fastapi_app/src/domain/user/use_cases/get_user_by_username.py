from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.user_repository import UserRepository
from schemas.user import User
from core.exceptions.domain_exceptions import UserNotFoundError

class GetUserByUsernameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, username: str) -> User:
        with self._database.session() as session:
            user = self._repo.get_by_username(session, username)
            if not user:
                raise UserNotFoundError(f"username={username}")
            return User.model_validate(user)