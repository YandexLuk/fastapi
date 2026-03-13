from typing import Optional
from fastapi import HTTPException, status
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.post_repository import PostRepository
from schemas.post import PostUpdate, Post


class UpdatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int, post_data: PostUpdate) -> Optional[Post]:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_id(session, post_id)
                if not existing:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Пост с id {post_id} не найден"
                    )

                updated = self._repo.update(session, post_id, post_data)
                return Post.model_validate(updated)
        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при обновлении поста: {e}")
            raise