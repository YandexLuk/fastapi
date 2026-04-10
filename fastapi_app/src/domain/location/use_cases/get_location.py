from typing import List
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.location_repository import LocationRepository
from schemas.location import Location

class GetLocationsUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self) -> List[Location]:
        with self._database.session() as session:
            locations = self._repo.get_all(session)
            return [Location.model_validate(loc) for loc in locations]