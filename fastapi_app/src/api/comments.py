from fastapi import APIRouter, status, HTTPException

from schemas.comment import Comment, CommentCreate, CommentUpdate
from domain.comment.use_cases.get_comment import GetCommentsUseCase
from domain.comment.use_cases.get_comment_id import GetCommentByIdUseCase
from domain.comment.use_cases.create_comment import CreateCommentUseCase
from domain.comment.use_cases.update_comment import UpdateCommentUseCase
from domain.comment.use_cases.delete_comment import DeleteCommentUseCase

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/", response_model=list[Comment], status_code=status.HTTP_200_OK)
async def get_comments():
    use_case = GetCommentsUseCase()
    return await use_case.execute()


@router.get("/{comment_id}", response_model=Comment, status_code=status.HTTP_200_OK)
async def get_comment_by_id(comment_id: int):
    use_case = GetCommentByIdUseCase()
    comment = await use_case.execute(comment_id=comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment


@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(comment_data: CommentCreate):
    use_case = CreateCommentUseCase()
    return await use_case.execute(comment_data=comment_data)


@router.put("/{comment_id}", response_model=Comment, status_code=status.HTTP_200_OK)
async def update_comment(comment_id: int, comment_data: CommentUpdate):
    use_case = UpdateCommentUseCase()
    comment = await use_case.execute(comment_id=comment_id, comment_data=comment_data)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment(comment_id: int):
    use_case = DeleteCommentUseCase()
    result = await use_case.execute(comment_id=comment_id)
    if not result["deleted"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return result