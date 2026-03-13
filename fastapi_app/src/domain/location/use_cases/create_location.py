from fastapi import HTTPException, status
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.location_repository import LocationRepository
from schemas.location import Location, LocationCreate


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_data: LocationCreate) -> Location:
        """Создать новую локацию"""
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_name(session, location_data.name)
                if existing:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Локация с названием '{location_data.name}' уже существует"
                    )

                new_location = self._repo.create(session, location_data)

                return Location.model_validate(new_location)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при создании локации: {e}")
            raise