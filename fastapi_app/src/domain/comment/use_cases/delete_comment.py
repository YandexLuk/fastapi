from fastapi import HTTPException, status
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comment_repository import CommentRepository


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> dict:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_id(session, comment_id)
                if not existing:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Комментарий с id {comment_id} не найден"
                    )

                deleted = self._repo.delete(session, comment_id)
                return {"deleted": deleted}
        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при удалении комментария: {e}")
            raise