from fastapi import APIRouter, status, HTTPException
from schemas.post import Post, PostCreate, PostUpdate
from domain.post.use_cases.get_post import GetPostsUseCase
from domain.post.use_cases.get_post_by_id import GetPostByIdUseCase
from domain.post.use_cases.create_post import CreatePostUseCase
from domain.post.use_cases.update_post import UpdatePostUseCase
from domain.post.use_cases.delete_post import DeletePostUseCase
from core.exceptions.domain_exceptions import (
    PostNotFoundError, PostAuthorNotFoundError
)

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=list[Post])
async def get_posts():
    return await GetPostsUseCase().execute()

@router.get("/{post_id}", response_model=Post)
async def get_post_by_id(post_id: int):
    try:
        return await GetPostByIdUseCase().execute(post_id=post_id)
    except PostNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)

@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostCreate):
    try:
        return await CreatePostUseCase().execute(post_data=post_data)
    except PostAuthorNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)

@router.put("/{post_id}", response_model=Post)
async def update_post(post_id: int, post_data: PostUpdate):
    try:
        return await UpdatePostUseCase().execute(post_id=post_id, post_data=post_data)
    except PostNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except PostAuthorNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)

@router.delete("/{post_id}")
async def delete_post(post_id: int):
    try:
        return await DeletePostUseCase().execute(post_id=post_id)
    except PostNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)