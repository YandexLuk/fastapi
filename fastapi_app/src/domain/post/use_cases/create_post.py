from fastapi import HTTPException, status
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.post_repository import PostRepository
from infrastructure.sqlite.repositories.user_repository import UserRepository
from infrastructure.sqlite.repositories.category_repository import CategoryRepository
from infrastructure.sqlite.repositories.location_repository import LocationRepository
from schemas.post import Post, PostCreate


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UserRepository()
        self._category_repo = CategoryRepository()
        self._location_repo = LocationRepository()

    async def execute(self, post_data: PostCreate) -> Post:
        """Создать новый пост"""
        try:
            with self._database.session() as session:
                author = self._user_repo.get_by_id(session, post_data.author_id)
                if not author:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Автор с id {post_data.author_id} не найден"
                    )

                if post_data.category_id is not None:
                    category = self._category_repo.get_by_id(session, post_data.category_id)
                    if not category:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Категория с id {post_data.category_id} не найдена"
                        )

                if post_data.location_id is not None:
                    location = self._location_repo.get_by_id(session, post_data.location_id)
                    if not location:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Локация с id {post_data.location_id} не найдена"
                        )

                new_post = self._repo.create(session, post_data)

                return Post.model_validate(new_post)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при создании поста: {e}")
            raise