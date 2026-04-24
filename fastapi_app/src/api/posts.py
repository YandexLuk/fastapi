from fastapi import APIRouter, status, HTTPException, Depends
from schemas.post import Post, PostCreate, PostUpdate
from domain.post.use_cases.get_post import GetPostsUseCase
from domain.post.use_cases.get_post_by_id import GetPostByIdUseCase
from domain.post.use_cases.create_post import CreatePostUseCase
from domain.post.use_cases.update_post import UpdatePostUseCase
from domain.post.use_cases.delete_post import DeletePostUseCase
from core.exceptions.domain_exceptions import (
    PostNotFoundError, PostAuthorNotFoundError
)
from core.exceptions.database_exceptions import PostNotFoundError as DBPostNotFoundError
from core.dependencies import get_current_user
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.post_repository import PostRepository
from core.logging_config import get_logger

logger = get_logger("posts")

router = APIRouter(prefix="/posts", tags=["Posts"])

_post_repo = PostRepository()


@router.get("/", response_model=list[Post])
async def get_posts():
    """Получить все посты. Публичный доступ."""
    return await GetPostsUseCase().execute()


@router.get("/{post_id}", response_model=Post)
async def get_post_by_id(post_id: int):
    """Получить пост по ID. Публичный доступ."""
    try:
        return await GetPostByIdUseCase().execute(post_id=post_id)
    except PostNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostCreate, current_user=Depends(get_current_user)):
    """
    Создать пост. Только для авторизованных пользователей.
    author_id автоматически берётся из JWT-токена.
    """
    # Переопределяем author_id из токена
    post_data = PostCreate(
        title=post_data.title,
        text=post_data.text,
        pub_date=post_data.pub_date,
        author_id=current_user.id,
        category_id=post_data.category_id,
        location_id=post_data.location_id,
    )
    try:
        result = await CreatePostUseCase().execute(post_data=post_data)
        logger.info("Пользователь '%s' создал пост (id=%s, title='%s')", current_user.username, result.id, result.title)
        return result
    except PostAuthorNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)


@router.put("/{post_id}", response_model=Post)
async def update_post(post_id: int, post_data: PostUpdate, current_user=Depends(get_current_user)):
    """
    Обновить пост. Только автор поста или администратор.
    """
    # Проверяем авторство
    try:
        with database.session() as session:
            post = _post_repo.get_by_id(session, post_id)
            if post.author_id != current_user.id and not current_user.is_superuser:
                logger.warning("Пользователь '%s' попытался редактировать чужой пост (id=%s)", current_user.username, post_id)
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Вы можете редактировать только свои посты",
                )
    except DBPostNotFoundError:
        raise HTTPException(status_code=404, detail=f"Пост с ID {post_id} не найден")
    try:
        result = await UpdatePostUseCase().execute(post_id=post_id, post_data=post_data)
        logger.info("Пользователь '%s' обновил пост (id=%s)", current_user.username, post_id)
        return result
    except PostNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except PostAuthorNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)


@router.delete("/{post_id}")
async def delete_post(post_id: int, current_user=Depends(get_current_user)):
    """
    Удалить пост. Только автор поста или администратор.
    """
    # Проверяем авторство
    try:
        with database.session() as session:
            post = _post_repo.get_by_id(session, post_id)
            if post.author_id != current_user.id and not current_user.is_superuser:
                logger.warning("Пользователь '%s' попытался удалить чужой пост (id=%s)", current_user.username, post_id)
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Вы можете удалять только свои посты",
                )
    except DBPostNotFoundError:
        raise HTTPException(status_code=404, detail=f"Пост с ID {post_id} не найден")
    try:
        result = await DeletePostUseCase().execute(post_id=post_id)
        logger.info("Пользователь '%s' удалил пост (id=%s)", current_user.username, post_id)
        return result
    except PostNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)