from typing import Optional
from fastapi import HTTPException, status
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comment_repository import CommentRepository
from schemas.comment import Comment


class GetCommentByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> Optional[Comment]:
        try:
            with self._database.session() as session:
                comment = self._repo.get_by_id(session, comment_id)
                if not comment:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Комментарий с id {comment_id} не найден"
                    )
                return Comment.model_validate(comment)
        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при получении комментария: {e}")
            raise