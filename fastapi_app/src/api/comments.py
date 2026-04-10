from fastapi import APIRouter, status, HTTPException
from schemas.comment import Comment, CommentCreate, CommentUpdate
from domain.comment.use_cases.get_comment import GetCommentsUseCase
from domain.comment.use_cases.get_comment_id import GetCommentByIdUseCase
from domain.comment.use_cases.create_comment import CreateCommentUseCase
from domain.comment.use_cases.update_comment import UpdateCommentUseCase
from domain.comment.use_cases.delete_comment import DeleteCommentUseCase
from core.exceptions.domain_exceptions import (
    CommentNotFoundError, PostAuthorNotFoundError, PostNotFoundError
)

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.get("/", response_model=list[Comment])
async def get_comments():
    return await GetCommentsUseCase().execute()

@router.get("/{comment_id}", response_model=Comment)
async def get_comment_by_id(comment_id: int):
    try:
        return await GetCommentByIdUseCase().execute(comment_id=comment_id)
    except CommentNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)

@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(comment_data: CommentCreate):
    try:
        return await CreateCommentUseCase().execute(comment_data=comment_data)
    except PostAuthorNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except PostNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)

@router.put("/{comment_id}", response_model=Comment)
async def update_comment(comment_id: int, comment_data: CommentUpdate):
    try:
        return await UpdateCommentUseCase().execute(comment_id=comment_id, comment_data=comment_data)
    except CommentNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)

@router.delete("/{comment_id}")
async def delete_comment(comment_id: int):
    try:
        return await DeleteCommentUseCase().execute(comment_id=comment_id)
    except CommentNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)