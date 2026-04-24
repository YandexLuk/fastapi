from fastapi import APIRouter, status, HTTPException, Depends
from schemas.comment import Comment, CommentCreate, CommentUpdate
from domain.comment.use_cases.get_comment import GetCommentsUseCase
from domain.comment.use_cases.get_comment_id import GetCommentByIdUseCase
from domain.comment.use_cases.create_comment import CreateCommentUseCase
from domain.comment.use_cases.update_comment import UpdateCommentUseCase
from domain.comment.use_cases.delete_comment import DeleteCommentUseCase
from core.exceptions.domain_exceptions import (
    CommentNotFoundError, PostAuthorNotFoundError, PostNotFoundError
)
from core.exceptions.database_exceptions import CommentNotFoundError as DBCommentNotFoundError
from core.dependencies import get_current_user
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comment_repository import CommentRepository
from core.logging_config import get_logger

logger = get_logger("comments")

router = APIRouter(prefix="/comments", tags=["Comments"])

_comment_repo = CommentRepository()


@router.get("/", response_model=list[Comment])
async def get_comments():
    """Получить все комментарии. Публичный доступ."""
    return await GetCommentsUseCase().execute()


@router.get("/{comment_id}", response_model=Comment)
async def get_comment_by_id(comment_id: int):
    """Получить комментарий по ID. Публичный доступ."""
    try:
        return await GetCommentByIdUseCase().execute(comment_id=comment_id)
    except CommentNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)


@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(comment_data: CommentCreate, current_user=Depends(get_current_user)):
    """
    Создать комментарий. Только для авторизованных пользователей.
    author_id автоматически берётся из JWT-токена.
    """
    # Переопределяем author_id из токена
    comment_data = CommentCreate(
        text=comment_data.text,
        post_id=comment_data.post_id,
        author_id=current_user.id,
    )
    try:
        result = await CreateCommentUseCase().execute(comment_data=comment_data)
        logger.info("Пользователь '%s' создал комментарий (id=%s, post_id=%s)", current_user.username, result.id, result.post_id)
        return result
    except PostAuthorNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except PostNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)


@router.put("/{comment_id}", response_model=Comment)
async def update_comment(comment_id: int, comment_data: CommentUpdate, current_user=Depends(get_current_user)):
    """
    Обновить комментарий. Только автор комментария или администратор.
    """
    # Проверяем авторство
    try:
        with database.session() as session:
            comment = _comment_repo.get_by_id(session, comment_id)
            if comment.author_id != current_user.id and not current_user.is_superuser:
                logger.warning("Пользователь '%s' попытался редактировать чужой комментарий (id=%s)", current_user.username, comment_id)
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Вы можете редактировать только свои комментарии",
                )
    except DBCommentNotFoundError:
        raise HTTPException(status_code=404, detail=f"Комментарий с ID {comment_id} не найден")
    try:
        result = await UpdateCommentUseCase().execute(comment_id=comment_id, comment_data=comment_data)
        logger.info("Пользователь '%s' обновил комментарий (id=%s)", current_user.username, comment_id)
        return result
    except CommentNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)


@router.delete("/{comment_id}")
async def delete_comment(comment_id: int, current_user=Depends(get_current_user)):
    """
    Удалить комментарий. Только автор комментария или администратор.
    """
    # Проверяем авторство
    try:
        with database.session() as session:
            comment = _comment_repo.get_by_id(session, comment_id)
            if comment.author_id != current_user.id and not current_user.is_superuser:
                logger.warning("Пользователь '%s' попытался удалить чужой комментарий (id=%s)", current_user.username, comment_id)
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Вы можете удалять только свои комментарии",
                )
    except DBCommentNotFoundError:
        raise HTTPException(status_code=404, detail=f"Комментарий с ID {comment_id} не найден")
    try:
        result = await DeleteCommentUseCase().execute(comment_id=comment_id)
        logger.info("Пользователь '%s' удалил комментарий (id=%s)", current_user.username, comment_id)
        return result
    except CommentNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)