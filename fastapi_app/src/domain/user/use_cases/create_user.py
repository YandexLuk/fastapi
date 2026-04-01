from fastapi import HTTPException, status
from passlib.context import CryptContext
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.user_repository import UserRepository
from schemas.user import User, UserCreate

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__ident="2b"
)

class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_data: UserCreate) -> User:
        """Создать нового пользователя"""
        try:
            with self._database.session() as session:
                existing_username = self._repo.get_by_username(session, user_data.username)
                if existing_username:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Пользователь с username '{user_data.username}' уже существует"
                    )

                if user_data.email:
                    existing_email = self._repo.get_by_email(session, user_data.email)
                    if existing_email:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Пользователь с email '{user_data.email}' уже существует"
                        )

                hashed_password = pwd_context.hash(user_data.password)

                user_dict = user_data.dict()
                user_dict['password'] = hashed_password

                from schemas.user import UserCreate as UserCreateSchema
                user_data_with_hash = UserCreateSchema(**user_dict)

                new_user = self._repo.create(session, user_dict)

                return User.model_validate(new_user)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при создании пользователя: {e}")
            raise