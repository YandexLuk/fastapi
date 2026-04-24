import logging
import sys


def setup_logging() -> None:
    """Настройка логирования приложения."""
    app_logger = logging.getLogger("app")

    if app_logger.handlers:
        return

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    app_logger.setLevel(logging.INFO)
    app_logger.addHandler(handler)
    app_logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    """Получить логгер для модуля."""
    return logging.getLogger(f"app.{name}")
