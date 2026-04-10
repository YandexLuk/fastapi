from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comment_repository import CommentRepository
from core.exceptions.database_exceptions import CommentNotFoundError as DBCommentNotFoundError
from core.exceptions.domain_exceptions import CommentNotFoundError

class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> dict:
        try:
            with self._database.session() as session:
                deleted = self._repo.delete(session, comment_id)
                return {"deleted": deleted}
        except DBCommentNotFoundError as e:
            raise CommentNotFoundError(f"id={comment_id}") from e