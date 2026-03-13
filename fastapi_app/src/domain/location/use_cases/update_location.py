from typing import Optional
from fastapi import HTTPException, status
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.location_repository import LocationRepository
from schemas.location import LocationUpdate, Location


class UpdateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int, location_data: LocationUpdate) -> Optional[Location]:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_id(session, location_id)
                if not existing:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Локация с id {location_id} не найдена"
                    )

                if location_data.name is not None:
                    name_exists = self._repo.get_by_name(session, location_data.name)
                    if name_exists and name_exists.id != location_id:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Локация с названием '{location_data.name}' уже существует"
                        )

                updated = self._repo.update(session, location_id, location_data)
                return Location.model_validate(updated)
        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при обновлении локации: {e}")
            raise