from fastapi import HTTPException, status
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.post_repository import PostRepository


class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> dict:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_id(session, post_id)
                if not existing:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Пост с id {post_id} не найден"
                    )

                deleted = self._repo.delete(session, post_id)
                return {"deleted": deleted}
        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при удалении поста: {e}")
            raise