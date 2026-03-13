from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from infrastructure.sqlite.models.users import User
from schemas.user import UserCreate, UserUpdate

class UserRepository:
    def __init__(self):
        self.model = User

    def get_by_id(self, session: Session, user_id: int) -> Optional[User]:
        """Получить пользователя по ID"""
        return session.get(self.model, user_id)

    def get_by_username(self, session: Session, username: str) -> Optional[User]:
        """Получить пользователя по username"""
        return session.query(self.model).filter(self.model.username == username).first()

    def get_all(self, session: Session) -> List[User]:
        """Получить всех пользователей"""
        return session.query(self.model).all()

    def get_by_email(self, session: Session, email: str) -> Optional[User]:
        """Получить пользователя по email"""
        return session.query(self.model).filter(self.model.email == email).first()

    def create(self, session: Session, user_data: dict) -> User:
        """Создать пользователя из словаря (уже с хэшированным паролем)"""
        from datetime import datetime

        user = self.model(
            username=user_data['username'],
            email=user_data.get('email', ""),
            password=user_data['password'],
            first_name=user_data.get('first_name', ""),
            last_name=user_data.get('last_name', ""),
            is_active=user_data.get('is_active', True),
            is_superuser=False,
            is_staff=False,
            date_joined=datetime.now(),
            last_login=None
        )
        session.add(user)
        session.flush()
        return user

    def update(self, session: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Обновить данные пользователя (частичное обновление)"""
        user = self.get_by_id(session, user_id)
        if not user:
            return None

        forbidden_fields = {'id', 'date_joined', 'is_superuser', 'is_staff'}

        update_data = user_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if field not in forbidden_fields and hasattr(user, field):
                if value is not None:
                    setattr(user, field, value)

        return user

    def delete(self, session: Session, user_id: int) -> bool:
        """Удалить пользователя по ID. Возвращает True, если удаление успешно."""
        user = self.get_by_id(session, user_id)
        if user:
            session.delete(user)
            return True
        return False