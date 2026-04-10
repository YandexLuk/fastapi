from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.post_repository import PostRepository
from schemas.post import Post
from core.exceptions.database_exceptions import PostNotFoundError as DBPostNotFoundError
from core.exceptions.domain_exceptions import PostNotFoundError

class GetPostByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> Post:
        try:
            with self._database.session() as session:
                post = self._repo.get_by_id(session, post_id)
                return Post.model_validate(post)
        except DBPostNotFoundError as e:
            raise PostNotFoundError(f"id={post_id}") from e