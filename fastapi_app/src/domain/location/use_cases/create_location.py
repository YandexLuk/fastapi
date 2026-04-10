from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.location_repository import LocationRepository
from schemas.location import Location, LocationCreate
from core.exceptions.database_exceptions import LocationAlreadyExistsError as DBLocationAlreadyExistsError
from core.exceptions.domain_exceptions import LocationAlreadyExistsError

class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_data: LocationCreate) -> Location:
        try:
            with self._database.session() as session:
                # Проверяем уникальность названия
                existing = self._repo.get_by_name(session, location_data.name)
                if existing:
                    raise LocationAlreadyExistsError(location_data.name)

                new_location = self._repo.create(session, location_data)
                return Location.model_validate(new_location)
        except DBLocationAlreadyExistsError as e:
            # Обогащаем контекстом и преобразуем в доменное исключение
            raise LocationAlreadyExistsError(location_data.name) from e