from passlib.context import CryptContext
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.user_repository import UserRepository
from schemas.user import User, UserCreate
from core.exceptions.database_exceptions import UserAlreadyExistsError as DBUserAlreadyExistsError
from core.exceptions.domain_exceptions import UserAlreadyExistsError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_data: UserCreate) -> User:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_username(session, user_data.username)
                if existing:
                    raise UserAlreadyExistsError("username", user_data.username)
                if user_data.email:
                    existing = self._repo.get_by_email(session, user_data.email)
                    if existing:
                        raise UserAlreadyExistsError("email", user_data.email)

                hashed = pwd_context.hash(user_data.password)
                user_dict = user_data.dict()
                user_dict['password'] = hashed

                new_user = self._repo.create(session, user_dict)
                return User.model_validate(new_user)
        except DBUserAlreadyExistsError as e:
            raise UserAlreadyExistsError("username", user_data.username) from e