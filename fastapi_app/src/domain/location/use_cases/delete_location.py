from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.location_repository import LocationRepository
from core.exceptions.database_exceptions import LocationNotFoundError as DBLocationNotFoundError
from core.exceptions.domain_exceptions import LocationNotFoundError

class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> dict:
        try:
            with self._database.session() as session:
                deleted = self._repo.delete(session, location_id)
                return {"deleted": deleted}
        except DBLocationNotFoundError as e:
            raise LocationNotFoundError(f"id={location_id}") from e