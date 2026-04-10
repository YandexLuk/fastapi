from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comment_repository import CommentRepository
from infrastructure.sqlite.repositories.user_repository import UserRepository
from infrastructure.sqlite.repositories.post_repository import PostRepository
from schemas.comment import Comment, CommentCreate
from core.exceptions.database_exceptions import (
    UserNotFoundError as DBUserNotFoundError,
    PostNotFoundError as DBPostNotFoundError,
    DatabaseError
)
from core.exceptions.domain_exceptions import (
    PostAuthorNotFoundError,
    PostNotFoundError
)

class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._comment_repo = CommentRepository()
        self._user_repo = UserRepository()
        self._post_repo = PostRepository()

    async def execute(self, comment_data: CommentCreate) -> Comment:
        try:
            with self._database.session() as session:
                # Проверяем существование автора
                try:
                    author = self._user_repo.get_by_id(session, comment_data.author_id)
                except DBUserNotFoundError:
                    raise PostAuthorNotFoundError(comment_data.author_id)

                # Проверяем существование поста
                try:
                    post = self._post_repo.get_by_id(session, comment_data.post_id)
                except DBPostNotFoundError:
                    raise PostNotFoundError(f"id={comment_data.post_id}")

                # Создаём комментарий
                new_comment = self._comment_repo.create(session, comment_data)
                return Comment.model_validate(new_comment)
        except DatabaseError as e:
            e.detail = f"{e.detail} (operation: create_comment, author_id: {comment_data.author_id}, post_id: {comment_data.post_id})"
            raise