from fastapi import APIRouter, status, HTTPException, Depends
from schemas.user import User, UserCreate, UserUpdate
from domain.user.use_cases.get_user import GetUsersUseCase
from domain.user.use_cases.get_user_by_id import GetUserByIdUseCase
from domain.user.use_cases.get_user_by_username import GetUserByUsernameUseCase
from domain.user.use_cases.create_user import CreateUserUseCase
from domain.user.use_cases.update_user import UpdateUserUseCase
from domain.user.use_cases.delete_user import DeleteUserUseCase
from core.exceptions.domain_exceptions import (
    UserNotFoundError, UserAlreadyExistsError
)
from core.dependencies import get_current_user, get_current_admin_user
from core.logging_config import get_logger

logger = get_logger("users")

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[User])
async def get_users(current_user=Depends(get_current_admin_user)):
    """Получить список всех пользователей. Только для администраторов."""
    logger.info("Админ '%s' запросил список пользователей", current_user.username)
    return await GetUsersUseCase().execute()


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    """
    Создать нового пользователя.
    Регистрация открыта для всех. Поле is_superuser по умолчанию False.
    """
    try:
        result = await CreateUserUseCase().execute(user_data=user_data)
        logger.info("Создан пользователь '%s' (id=%s, admin=%s)", result.username, result.id, result.is_superuser)
        return result
    except UserAlreadyExistsError as e:
        logger.warning("Попытка создать существующего пользователя '%s'", user_data.username)
        raise HTTPException(status_code=409, detail=e.detail)


@router.get("/{user_id}", response_model=User)
async def get_user_by_id(user_id: int, current_user=Depends(get_current_user)):
    """Получить пользователя по ID. Для авторизованных пользователей."""
    try:
        return await GetUserByIdUseCase().execute(user_id=user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)


@router.get("/by-username/{username}", response_model=User)
async def get_user_by_username(username: str, current_user=Depends(get_current_user)):
    """Получить пользователя по username. Для авторизованных пользователей."""
    try:
        return await GetUserByUsernameUseCase().execute(username=username)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_data: UserUpdate, current_user=Depends(get_current_user)):
    """
    Обновить данные пользователя.
    Только сам пользователь может обновлять свой профиль, или администратор.
    """
    if current_user.id != user_id and not current_user.is_superuser:
        logger.warning("Пользователь '%s' попытался обновить чужой профиль (id=%s)", current_user.username, user_id)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы можете обновлять только свой профиль",
        )
    try:
        result = await UpdateUserUseCase().execute(user_id=user_id, user_data=user_data)
        logger.info("Пользователь '%s' обновил профиль (id=%s)", current_user.username, user_id)
        return result
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=e.detail)


@router.delete("/{user_id}")
async def delete_user(user_id: int, current_user=Depends(get_current_admin_user)):
    """Удалить пользователя. Только для администраторов."""
    try:
        result = await DeleteUserUseCase().execute(user_id=user_id)
        logger.info("Админ '%s' удалил пользователя (id=%s)", current_user.username, user_id)
        return result
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)