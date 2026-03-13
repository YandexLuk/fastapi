from typing import Optional
from fastapi import HTTPException, status
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comment_repository import CommentRepository
from schemas.comment import CommentUpdate, Comment


class UpdateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int, comment_data: CommentUpdate) -> Optional[Comment]:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_id(session, comment_id)
                if not existing:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Комментарий с id {comment_id} не найден"
                    )

                updated = self._repo.update(session, comment_id, comment_data)
                return Comment.model_validate(updated)
        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при обновлении комментария: {e}")
            raise