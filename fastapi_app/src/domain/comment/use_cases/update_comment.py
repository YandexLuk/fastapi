from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comment_repository import CommentRepository
from schemas.comment import Comment, CommentUpdate
from core.exceptions.database_exceptions import CommentNotFoundError as DBCommentNotFoundError
from core.exceptions.domain_exceptions import CommentNotFoundError

class UpdateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int, comment_data: CommentUpdate) -> Comment:
        try:
            with self._database.session() as session:
                # Проверяем существование комментария
                try:
                    existing_comment = self._repo.get_by_id(session, comment_id)
                except DBCommentNotFoundError:
                    raise CommentNotFoundError(f"id={comment_id}")

                updated_comment = self._repo.update(session, comment_id, comment_data)
                return Comment.model_validate(updated_comment)
        except DBCommentNotFoundError as e:
            raise CommentNotFoundError(f"id={comment_id}") from e