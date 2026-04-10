from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from infrastructure.sqlite.models.location import Location
from schemas.location import LocationCreate, LocationUpdate
from core.exceptions.database_exceptions import (
    DatabaseError, LocationNotFoundError, LocationAlreadyExistsError
)

class LocationRepository:
    def __init__(self):
        self.model = Location

    def get_by_id(self, session: Session, location_id: int) -> Location:
        try:
            location = session.get(self.model, location_id)
            if location is None:
                raise LocationNotFoundError(f"Location with id {location_id} not found")
            return location
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error: {e}")

    def get_by_name(self, session: Session, name: str) -> Optional[Location]:
        try:
            return session.query(self.model).filter(self.model.name == name).first()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error: {e}")

    def get_all(self, session: Session) -> List[Location]:
        try:
            return session.query(self.model).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error: {e}")

    def create(self, session: Session, location_data: LocationCreate) -> Location:
        try:
            location = self.model(
                name=location_data.name,
                is_published=True,
                created_at=datetime.now()
            )
            session.add(location)
            session.flush()
            return location
        except IntegrityError as e:
            if "name" in str(e.orig):
                raise LocationAlreadyExistsError(f"Location with name '{location_data.name}' already exists")
            raise DatabaseError(f"Integrity error: {e}")
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error: {e}")

    def update(self, session: Session, location_id: int, location_data: LocationUpdate) -> Location:
        try:
            location = self.get_by_id(session, location_id)
            update_data = location_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(location, field) and value is not None:
                    setattr(location, field, value)
            session.flush()
            return location
        except IntegrityError as e:
            if "name" in str(e.orig):
                raise LocationAlreadyExistsError("Location with this name already exists")
            raise DatabaseError(f"Integrity error: {e}")
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error: {e}")

    def delete(self, session: Session, location_id: int) -> bool:
        try:
            location = self.get_by_id(session, location_id)
            session.delete(location)
            return True
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error: {e}")