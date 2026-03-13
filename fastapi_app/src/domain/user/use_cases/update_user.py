from typing import Optional
from fastapi import HTTPException, status
from passlib.context import CryptContext
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.user_repository import UserRepository
from schemas.user import UserUpdate, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UpdateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Обновить данные пользователя"""
        try:
            with self._database.session() as session:
                existing_user = self._repo.get_by_id(session, user_id)
                if not existing_user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Пользователь с id {user_id} не найден"
                    )

                if user_data.username is not None and user_data.username != existing_user.username:
                    username_exists = self._repo.get_by_username(session, user_data.username)
                    if username_exists:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Пользователь с username '{user_data.username}' уже существует"
                        )

                if user_data.email is not None and user_data.email != existing_user.email:
                    email_exists = self._repo.get_by_email(session, user_data.email)
                    if email_exists:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Пользователь с email '{user_data.email}' уже существует"
                        )

                update_dict = user_data.dict(exclude_unset=True)
                if "password" in update_dict:
                    update_dict["password"] = pwd_context.hash(update_dict["password"])

                updated_user_data = UserUpdate(**update_dict)

                updated_user = self._repo.update(session, user_id, updated_user_data)
                return User.model_validate(updated_user)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при обновлении пользователя {user_id}: {e}")
            raise