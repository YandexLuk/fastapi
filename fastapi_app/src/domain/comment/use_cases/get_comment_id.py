from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comment_repository import CommentRepository
from schemas.comment import Comment
from core.exceptions.database_exceptions import CommentNotFoundError as DBCommentNotFoundError
from core.exceptions.domain_exceptions import CommentNotFoundError

class GetCommentByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> Comment:
        try:
            with self._database.session() as session:
                comment = self._repo.get_by_id(session, comment_id)
                return Comment.model_validate(comment)
        except DBCommentNotFoundError as e:
            raise CommentNotFoundError(f"id={comment_id}") from e