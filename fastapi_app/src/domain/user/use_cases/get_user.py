from typing import List
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.user_repository import UserRepository
from schemas.user import User

class GetUsersUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self) -> List[User]:
        """Получить всех пользователей"""
        try:
            with self._database.session() as session:
                users = self._repo.get_all(session)
                return [User.model_validate(u) for u in users]
        except Exception as e:
            print(f"Ошибка при получении пользователей: {e}")
            raise