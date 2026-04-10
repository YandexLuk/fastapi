from fastapi import APIRouter, status, HTTPException
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

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[User])
async def get_users():
    return await GetUsersUseCase().execute()

@router.get("/{user_id}", response_model=User)
async def get_user_by_id(user_id: int):
    try:
        return await GetUserByIdUseCase().execute(user_id=user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)

@router.get("/by-username/{username}", response_model=User)
async def get_user_by_username(username: str):
    try:
        return await GetUserByUsernameUseCase().execute(username=username)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    try:
        return await CreateUserUseCase().execute(user_data=user_data)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=e.detail)

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_data: UserUpdate):
    try:
        return await UpdateUserUseCase().execute(user_id=user_id, user_data=user_data)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=e.detail)

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    try:
        return await DeleteUserUseCase().execute(user_id=user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)