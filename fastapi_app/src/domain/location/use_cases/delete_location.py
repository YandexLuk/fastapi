from fastapi import HTTPException, status
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.location_repository import LocationRepository


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> dict:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_id(session, location_id)
                if not existing:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Локация с id {location_id} не найдена"
                    )

                deleted = self._repo.delete(session, location_id)
                return {"deleted": deleted}
        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при удалении локации: {e}")
            raise