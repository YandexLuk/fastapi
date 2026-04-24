from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from infrastructure.sqlite.models.users import User
from schemas.user import UserUpdate
from core.exceptions.database_exceptions import (
    DatabaseError, UserNotFoundError, UserAlreadyExistsError
)

class UserRepository:
    def __init__(self):
        self.model = User

    def get_by_id(self, session: Session, user_id: int) -> User:
        try:
            user = session.get(self.model, user_id)
            if user is None:
                raise UserNotFoundError(f"User with id {user_id} not found")
            return user
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error while fetching user by id: {e}")

    def get_by_username(self, session: Session, username: str) -> Optional[User]:
        try:
            return session.query(self.model).filter(self.model.username == username).first()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error while fetching user by username: {e}")

    def get_by_email(self, session: Session, email: str) -> Optional[User]:
        try:
            return session.query(self.model).filter(self.model.email == email).first()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error while fetching user by email: {e}")

    def get_all(self, session: Session) -> List[User]:
        try:
            return session.query(self.model).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error while fetching all users: {e}")

    def create(self, session: Session, user_data: dict) -> User:
        try:
            user = self.model(
                username=user_data['username'],
                email=user_data.get('email', ""),
                password=user_data['password'],
                first_name=user_data.get('first_name', ""),
                last_name=user_data.get('last_name', ""),
                is_active=user_data.get('is_active', True),
                is_superuser=user_data.get('is_superuser', False),
                is_staff=False,
                date_joined=datetime.now(),
                last_login=None
            )
            session.add(user)
            session.flush()
            return user
        except IntegrityError as e:
            error_msg = str(e.orig) if e.orig else str(e)
            if "username" in error_msg:
                raise UserAlreadyExistsError(f"Username '{user_data['username']}' already exists")
            elif "email" in error_msg:
                raise UserAlreadyExistsError(f"Email '{user_data['email']}' already exists")
            raise DatabaseError(f"Integrity error: {e}")
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error while creating user: {e}")

    def update(self, session: Session, user_id: int, user_data: UserUpdate) -> User:
        try:
            user = self.get_by_id(session, user_id)
            update_data = user_data.model_dump(exclude_unset=True)
            forbidden_fields = {'id', 'date_joined', 'is_superuser', 'is_staff'}
            for field, value in update_data.items():
                if field not in forbidden_fields and value is not None:
                    setattr(user, field, value)
            session.flush()
            return user
        except IntegrityError as e:
            error_msg = str(e.orig) if e.orig else str(e)
            if "username" in error_msg:
                raise UserAlreadyExistsError("Username already exists")
            elif "email" in error_msg:
                raise UserAlreadyExistsError("Email already exists")
            raise DatabaseError(f"Integrity error: {e}")
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error while updating user: {e}")

    def delete(self, session: Session, user_id: int) -> bool:
        try:
            user = self.get_by_id(session, user_id)
            session.delete(user)
            return True
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error while deleting user: {e}")