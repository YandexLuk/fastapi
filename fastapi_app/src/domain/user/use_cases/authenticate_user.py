from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.user_repository import UserRepository
from core.security import verify_password
from core.exceptions.auth_exceptions import InvalidCredentialsError


class AuthenticateUserUseCase:
    """
    Аутентификация пользователя по username и password.
    Проверяет существование пользователя и корректность пароля.
    """

    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, username: str, password: str) -> dict:
        """
        Возвращает словарь с данными пользователя при успешной аутентификации.
        Выбрасывает InvalidCredentialsError при неверных данных.
        """
        with self._database.session() as session:
            user = self._repo.get_by_username(session, username)
            if user is None:
                raise InvalidCredentialsError()

            if not verify_password(password, user.password):
                raise InvalidCredentialsError()

            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_superuser": user.is_superuser,
            }
