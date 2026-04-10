class AppException(Exception):
    """Базовое исключение приложения."""
    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(self.detail)