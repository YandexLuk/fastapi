from fastapi import APIRouter, status, HTTPException

from schemas.user import User, UserCreate, UserUpdate
from domain.user.use_cases.get_user import GetUsersUseCase
from domain.user.use_cases.get_user_by_id import GetUserByIdUseCase
from domain.user.use_cases.get_user_by_username import GetUserByUsernameUseCase
from domain.user.use_cases.create_user import CreateUserUseCase
from domain.user.use_cases.update_user import UpdateUserUseCase
from domain.user.use_cases.delete_user import DeleteUserUseCase

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[User], status_code=status.HTTP_200_OK)
async def get_users():
    use_case = GetUsersUseCase()
    return await use_case.execute()


@router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int):
    use_case = GetUserByIdUseCase()
    user = await use_case.execute(user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/by-username/{username}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user_by_username(username: str):
    use_case = GetUserByUsernameUseCase()
    user = await use_case.execute(username=username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    use_case = CreateUserUseCase()
    return await use_case.execute(user_data=user_data)


@router.put("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user_data: UserUpdate):
    use_case = UpdateUserUseCase()
    user = await use_case.execute(user_id=user_id, user_data=user_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int):
    use_case = DeleteUserUseCase()
    result = await use_case.execute(user_id=user_id)
    if not result["deleted"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return result