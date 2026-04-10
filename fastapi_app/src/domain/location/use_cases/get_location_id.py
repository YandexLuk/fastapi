from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.location_repository import LocationRepository
from schemas.location import Location
from core.exceptions.database_exceptions import LocationNotFoundError as DBLocationNotFoundError
from core.exceptions.domain_exceptions import LocationNotFoundError

class GetLocationByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> Location:
        try:
            with self._database.session() as session:
                location = self._repo.get_by_id(session, location_id)
                return Location.model_validate(location)
        except DBLocationNotFoundError as e:
            raise LocationNotFoundError(f"id={location_id}") from e