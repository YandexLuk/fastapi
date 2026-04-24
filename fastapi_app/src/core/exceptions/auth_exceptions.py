from .base import AppException


class InvalidCredentialsError(AppException):
    """Неверные учётные данные (логин или пароль)."""
    def __init__(self):
        super().__init__("Неверное имя пользователя или пароль")


class InsufficientPermissionsError(AppException):
    """Недостаточно прав для выполнения операции."""
    def __init__(self, detail: str = "Недостаточно прав для выполнения данной операции"):
        super().__init__(detail)


class TokenExpiredError(AppException):
    """JWT-токен истёк."""
    def __init__(self):
        super().__init__("Токен истёк, пожалуйста авторизуйтесь заново")


class InvalidTokenError(AppException):
    """Невалидный JWT-токен."""
    def __init__(self):
        super().__init__("Невалидный токен авторизации")
