from datetime import timedelta

from fastapi import APIRouter, HTTPException, status

from schemas.auth import AuthCredential, Token
from domain.user.use_cases.authenticate_user import AuthenticateUserUseCase
from core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from core.exceptions.auth_exceptions import InvalidCredentialsError
from core.logging_config import get_logger

logger = get_logger("auth")

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
async def login(credentials: AuthCredential):
    """
    Аутентификация пользователя и выдача JWT access-токена.
    Принимает login и password в JSON-теле запроса.
    """
    try:
        user_data = await AuthenticateUserUseCase().execute(
            username=credentials.login,
            password=credentials.password,
        )
    except InvalidCredentialsError as e:
        logger.warning("Неудачная попытка входа для пользователя '%s'", credentials.login)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user_data["username"],
            "user_id": user_data["id"],
        },
        expires_delta=access_token_expires,
    )

    logger.info("Пользователь '%s' (id=%s) успешно авторизован", user_data["username"], user_data["id"])
    return Token(access_token=access_token, token_type="bearer")
