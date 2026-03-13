from fastapi import HTTPException, status
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.user_repository import UserRepository

class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> dict:
        """Удалить пользователя по ID"""
        try:
            with self._database.session() as session:
                user = self._repo.get_by_id(session, user_id)
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Пользователь с id {user_id} не найден"
                    )

                deleted = self._repo.delete(session, user_id)
                if not deleted:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось удалить пользователя"
                    )

                return {"deleted": True, "user_id": user_id}

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при удалении пользователя {user_id}: {e}")
            raise