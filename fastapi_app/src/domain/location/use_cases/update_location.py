from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.location_repository import LocationRepository
from schemas.location import Location, LocationUpdate
from core.exceptions.database_exceptions import (
    LocationNotFoundError as DBLocationNotFoundError,
    LocationAlreadyExistsError as DBLocationAlreadyExistsError
)
from core.exceptions.domain_exceptions import (
    LocationNotFoundError,
    LocationAlreadyExistsError
)

class UpdateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int, location_data: LocationUpdate) -> Location:
        try:
            with self._database.session() as session:
                # Проверяем существование локации
                try:
                    existing_location = self._repo.get_by_id(session, location_id)
                except DBLocationNotFoundError:
                    raise LocationNotFoundError(f"id={location_id}")

                # Если меняется название, проверяем уникальность
                if location_data.name is not None and location_data.name != existing_location.name:
                    same_name = self._repo.get_by_name(session, location_data.name)
                    if same_name:
                        raise LocationAlreadyExistsError(location_data.name)

                updated_location = self._repo.update(session, location_id, location_data)
                return Location.model_validate(updated_location)
        except DBLocationAlreadyExistsError as e:
            raise LocationAlreadyExistsError(location_data.name) from e