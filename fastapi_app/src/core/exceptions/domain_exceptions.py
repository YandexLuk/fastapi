from .base import AppException

class DomainError(AppException):
    """Базовое доменное исключение."""
    pass

# Пользователи
class UserNotFoundError(DomainError):
    def __init__(self, user_id: int):
        super().__init__(f"Пользователь с ID {user_id} не найден")

class UserAlreadyExistsError(DomainError):
    def __init__(self, field: str, value: str):
        super().__init__(f"Пользователь с {field} '{value}' уже существует")

# Категории
class CategoryNotFoundError(DomainError):
    def __init__(self, category_id: int):
        super().__init__(f"Категория с ID {category_id} не найдена")

class CategoryAlreadyExistsError(DomainError):
    def __init__(self, field: str, value: str):
        super().__init__(f"Категория с {field} '{value}' уже существует")

# Локации
class LocationNotFoundError(DomainError):
    def __init__(self, location_id: int):
        super().__init__(f"Локация с ID {location_id} не найдена")

class LocationAlreadyExistsError(DomainError):
    def __init__(self, name: str):
        super().__init__(f"Локация с названием '{name}' уже существует")

# Посты
class PostNotFoundError(DomainError):
    def __init__(self, post_id: int):
        super().__init__(f"Пост с ID {post_id} не найден")

class PostAuthorNotFoundError(DomainError):
    def __init__(self, author_id: int):
        super().__init__(f"Автор с ID {author_id} не найден")

# Комментарии
class CommentNotFoundError(DomainError):
    def __init__(self, comment_id: int):
        super().__init__(f"Комментарий с ID {comment_id} не найден")

# Валидация
class ValidationError(DomainError):
    pass