from typing import Optional
from fastapi import HTTPException, status
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.user_repository import UserRepository
from schemas.user import User

class GetUserByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID"""
        try:
            with self._database.session() as session:
                user = self._repo.get_by_id(session, user_id)
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Пользователь с id {user_id} не найден"
                    )
                return User.model_validate(user)
        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при получении пользователя по id {user_id}: {e}")
            raise