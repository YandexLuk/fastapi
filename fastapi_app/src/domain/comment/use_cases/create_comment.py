from fastapi import HTTPException, status
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comment_repository import CommentRepository
from infrastructure.sqlite.repositories.user_repository import UserRepository
from infrastructure.sqlite.repositories.post_repository import PostRepository
from schemas.comment import Comment, CommentCreate


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._user_repo = UserRepository()
        self._post_repo = PostRepository()

    async def execute(self, comment_data: CommentCreate) -> Comment:
        """Создать новый комментарий"""
        try:
            with self._database.session() as session:
                author = self._user_repo.get_by_id(session, comment_data.author_id)
                if not author:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Автор с id {comment_data.author_id} не найден"
                    )

                post = self._post_repo.get_by_id(session, comment_data.post_id)
                if not post:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Пост с id {comment_data.post_id} не найден"
                    )

                new_comment = self._repo.create(session, comment_data)

                return Comment.model_validate(new_comment)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при создании комментария: {e}")
            raise