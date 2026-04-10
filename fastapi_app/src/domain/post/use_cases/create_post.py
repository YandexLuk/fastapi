from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.post_repository import PostRepository
from infrastructure.sqlite.repositories.user_repository import UserRepository
from schemas.post import Post, PostCreate
from core.exceptions.database_exceptions import (
    DatabaseError, UserNotFoundError as DBUserNotFoundError
)
from core.exceptions.domain_exceptions import PostAuthorNotFoundError

class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._post_repo = PostRepository()
        self._user_repo = UserRepository()

    async def execute(self, post_data: PostCreate) -> Post:
        try:
            with self._database.session() as session:
                # Проверяем существование автора
                try:
                    author = self._user_repo.get_by_id(session, post_data.author_id)
                except DBUserNotFoundError:
                    raise PostAuthorNotFoundError(post_data.author_id)

                # Создаём пост
                new_post = self._post_repo.create(session, post_data)
                return Post.model_validate(new_post)
        except DatabaseError as e:
            # Обогащаем контекстом и пробрасываем дальше
            e.detail = f"{e.detail} (operation: create_post, author_id: {post_data.author_id})"
            raise