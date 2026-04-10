from typing import List
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.post_repository import PostRepository
from schemas.post import Post

class GetPostsUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self) -> List[Post]:
        with self._database.session() as session:
            posts = self._repo.get_all(session)
            return [Post.model_validate(p) for p in posts]