from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

from core.security import SECRET_KEY, ALGORITHM
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.user_repository import UserRepository
from infrastructure.sqlite.models.users import User

bearer_scheme = HTTPBearer()

_user_repo = UserRepository()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> "_UserSnapshot":

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Невалидный токен авторизации",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        user_id: int | None = payload.get("user_id")
        if username is None or user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    with database.session() as session:
        user = _user_repo.get_by_username(session, username)
        if user is None:
            raise credentials_exception

        user_data = _UserSnapshot(
            id=user.id,
            username=user.username,
            email=user.email,
            is_superuser=user.is_superuser,
            is_staff=user.is_staff,
            is_active=user.is_active,
        )

    if not user_data.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Аккаунт деактивирован",
        )

    return user_data


def get_current_admin_user(
    current_user: "_UserSnapshot" = Depends(get_current_user),
) -> "_UserSnapshot":
    """
    Проверяет, что текущий пользователь — администратор (is_superuser=True).
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав. Требуются права администратора.",
        )
    return current_user


class _UserSnapshot:

    def __init__(
        self,
        id: int,
        username: str,
        email: str,
        is_superuser: bool,
        is_staff: bool,
        is_active: bool,
    ):
        self.id = id
        self.username = username
        self.email = email
        self.is_superuser = is_superuser
        self.is_staff = is_staff
        self.is_active = is_active
