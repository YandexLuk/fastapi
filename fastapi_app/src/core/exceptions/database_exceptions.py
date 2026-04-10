from .base import AppException

class DatabaseError(AppException):
    """Общая ошибка базы данных."""
    pass

class EntityNotFoundError(DatabaseError):
    """Сущность не найдена в БД."""
    pass

class EntityAlreadyExistsError(DatabaseError):
    """Сущность уже существует (нарушение уникальности)."""
    pass

class UserNotFoundError(EntityNotFoundError):
    pass

class UserAlreadyExistsError(EntityAlreadyExistsError):
    pass

class CategoryNotFoundError(EntityNotFoundError):
    pass

class CategoryAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"Category with {field} '{value}' already exists")

class LocationNotFoundError(EntityNotFoundError):
    pass

class LocationAlreadyExistsError(EntityAlreadyExistsError):
    pass

class PostNotFoundError(EntityNotFoundError):
    pass

class CommentNotFoundError(EntityNotFoundError):
    pass