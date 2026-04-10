from passlib.context import CryptContext
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.user_repository import UserRepository
from schemas.user import User, UserUpdate
from core.exceptions.database_exceptions import UserNotFoundError as DBUserNotFoundError, UserAlreadyExistsError as DBUserAlreadyExistsError
from core.exceptions.domain_exceptions import UserNotFoundError, UserAlreadyExistsError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UpdateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, user_data: UserUpdate) -> User:
        try:
            with self._database.session() as session:
                # Проверяем существование пользователя
                try:
                    self._repo.get_by_id(session, user_id)
                except DBUserNotFoundError:
                    raise UserNotFoundError(f"id={user_id}")

                # Проверка уникальности при изменении username/email
                if user_data.username:
                    existing = self._repo.get_by_username(session, user_data.username)
                    if existing and existing.id != user_id:
                        raise UserAlreadyExistsError("username", user_data.username)
                if user_data.email:
                    existing = self._repo.get_by_email(session, user_data.email)
                    if existing and existing.id != user_id:
                        raise UserAlreadyExistsError("email", user_data.email)

                # Хэширование пароля, если передан
                update_dict = user_data.dict(exclude_unset=True)
                if "password" in update_dict:
                    update_dict["password"] = pwd_context.hash(update_dict["password"])

                updated_user_data = UserUpdate(**update_dict)
                updated_user = self._repo.update(session, user_id, updated_user_data)
                return User.model_validate(updated_user)
        except DBUserAlreadyExistsError as e:
            # Определяем, какое поле вызвало конфликт
            if "username" in str(e):
                raise UserAlreadyExistsError("username", user_data.username)
            elif "email" in str(e):
                raise UserAlreadyExistsError("email", user_data.email)
            raise