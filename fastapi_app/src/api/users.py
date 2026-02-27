from fastapi import APIRouter, HTTPException, status
from src.schemas.user import User, UserCreate, UserUpdate
from typing import List, Optional

router = APIRouter(prefix="/users", tags=["users"])

users_db = []
user_id_counter = 1


@router.get("/", response_model=list[User])
def read_users():
    """Получить всех пользователей"""
    return users_db


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int):
    """Получить пользователя по ID"""
    for user in users_db:
        if user.id == user_id:
            return user

    raise HTTPException(status_code=404, detail="User not found")


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    """Создать нового пользователя"""
    global user_id_counter

    new_user = User(
        id=user_id_counter,
        username=user.username,
        email=user.email
    )

    users_db.append(new_user)
    user_id_counter += 1

    return new_user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate):
    """Обновить пользователя по ID"""
    # Ищем пользователя в списке
    for i, existing_user in enumerate(users_db):
        if existing_user.id == user_id:
            update_data = user_update.dict(exclude_unset=True)

            updated_user = User(
                id=existing_user.id,
                username=update_data.get("username", existing_user.username),
                email=update_data.get("email", existing_user.email)
            )

            # Заменяем в списке
            users_db[i] = updated_user

            return updated_user

    # Если пользователь не найден
    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    """Удалить пользователя по ID"""
    for i, user in enumerate(users_db):
        if user.id == user_id:
            users_db.pop(i)
            return None

    raise HTTPException(status_code=404, detail="User not found")