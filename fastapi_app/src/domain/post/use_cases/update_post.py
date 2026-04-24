from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.post_repository import PostRepository
from infrastructure.sqlite.repositories.user_repository import UserRepository
from schemas.post import Post, PostUpdate
from core.exceptions.database_exceptions import (
    PostNotFoundError as DBPostNotFoundError,
    UserNotFoundError as DBUserNotFoundError,
    DatabaseError
)
from core.exceptions.domain_exceptions import (
    PostNotFoundError,
    PostAuthorNotFoundError
)

class UpdatePostUseCase:
    def __init__(self):
        self._database = database
        self._post_repo = PostRepository()
        self._user_repo = UserRepository()

    async def execute(self, post_id: int, post_data: PostUpdate) -> Post:
        try:
            with self._database.session() as session:
                # Проверяем существование поста
                try:
                    existing_post = self._post_repo.get_by_id(session, post_id)
                except DBPostNotFoundError:
                    raise PostNotFoundError(f"id={post_id}")

                # Обновляем пост
                updated_post = self._post_repo.update(session, post_id, post_data)
                return Post.model_validate(updated_post)
        except DatabaseError as e:
            e.detail = f"{e.detail} (operation: update_post, post_id: {post_id})"
            raise