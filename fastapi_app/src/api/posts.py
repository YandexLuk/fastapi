from fastapi import APIRouter, status, HTTPException

from schemas.post import Post, PostCreate, PostUpdate
from domain.post.use_cases.get_post import GetPostsUseCase
from domain.post.use_cases.get_post_by_id import GetPostByIdUseCase
from domain.post.use_cases.create_post import CreatePostUseCase
from domain.post.use_cases.update_post import UpdatePostUseCase
from domain.post.use_cases.delete_post import DeletePostUseCase

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[Post], status_code=status.HTTP_200_OK)
async def get_posts():
    use_case = GetPostsUseCase()
    return await use_case.execute()


@router.get("/{post_id}", response_model=Post, status_code=status.HTTP_200_OK)
async def get_post_by_id(post_id: int):
    use_case = GetPostByIdUseCase()
    post = await use_case.execute(post_id=post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostCreate):
    use_case = CreatePostUseCase()
    return await use_case.execute(post_data=post_data)


@router.put("/{post_id}", response_model=Post, status_code=status.HTTP_200_OK)
async def update_post(post_id: int, post_data: PostUpdate):
    use_case = UpdatePostUseCase()
    post = await use_case.execute(post_id=post_id, post_data=post_data)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int):
    use_case = DeletePostUseCase()
    result = await use_case.execute(post_id=post_id)
    if not result["deleted"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return result