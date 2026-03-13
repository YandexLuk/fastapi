from typing import List
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comment_repository import CommentRepository
from schemas.comment import Comment


class GetCommentsUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self) -> List[Comment]:
        try:
            with self._database.session() as session:
                comments = self._repo.get_all(session)
                return [Comment.model_validate(c) for c in comments]
        except Exception as e:
            print(f"Ошибка при получении комментариев: {e}")
            raise