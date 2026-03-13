from fastapi import APIRouter, status, HTTPException

from schemas.category import Category, CategoryCreate, CategoryUpdate
from domain.category.use_cases.get_category import GetCategoriesUseCase
from domain.category.use_cases.get_category_by_id import GetCategoryByIdUseCase
from domain.category.use_cases.create_category import CreateCategoryUseCase
from domain.category.use_cases.update_category import UpdateCategoryUseCase
from domain.category.use_cases.delete_category import DeleteCategoryUseCase

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[Category], status_code=status.HTTP_200_OK)
async def get_categories():
    use_case = GetCategoriesUseCase()
    return await use_case.execute()


@router.get("/{category_id}", response_model=Category, status_code=status.HTTP_200_OK)
async def get_category_by_id(category_id: int):
    use_case = GetCategoryByIdUseCase()
    category = await use_case.execute(category_id=category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(category_data: CategoryCreate):
    use_case = CreateCategoryUseCase()
    return await use_case.execute(category_data=category_data)


@router.put("/{category_id}", response_model=Category, status_code=status.HTTP_200_OK)
async def update_category(category_id: int, category_data: CategoryUpdate):
    use_case = UpdateCategoryUseCase()
    category = await use_case.execute(category_id=category_id, category_data=category_data)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(category_id: int):
    use_case = DeleteCategoryUseCase()
    result = await use_case.execute(category_id=category_id)
    if not result["deleted"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return result