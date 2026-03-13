from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from infrastructure.sqlite.models.location import Location
from schemas.location import LocationCreate, LocationUpdate

class LocationRepository:
    def __init__(self):
        self.model = Location

    def get_by_id(self, session: Session, location_id: int) -> Optional[Location]:
        return session.get(self.model, location_id)

    def get_all(self, session: Session) -> List[Location]:
        return session.query(self.model).all()

    def create(self, session: Session, location_data: LocationCreate) -> Location:
        location = self.model(
            name=location_data.name,
            is_published=True,
            created_at=datetime.now()
        )
        session.add(location)
        session.flush()
        return location

    def update(self, session: Session, location_id: int, location_data: LocationUpdate) -> Optional[Location]:
        location = self.get_by_id(session, location_id)
        if not location:
            return None

        forbidden_fields = {'id', 'created_at'}
        update_data = location_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if field not in forbidden_fields and hasattr(location, field):
                if value is not None:
                    setattr(location, field, value)

        return location

    def delete(self, session: Session, location_id: int) -> bool:
        location = self.get_by_id(session, location_id)
        if location:
            session.delete(location)
            return True
        return False