from typing import Optional
from fastapi import HTTPException, status
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.user_repository import UserRepository
from schemas.user import User

class GetUserByUsernameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, username: str) -> Optional[User]:
        """Получить пользователя по username"""
        try:
            with self._database.session() as session:
                user = self._repo.get_by_username(session, username)
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Пользователь с username '{username}' не найден"
                    )
                return User.model_validate(user)
        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при получении пользователя по username {username}: {e}")
            raise