from fastapi import APIRouter, status, HTTPException
from schemas.category import Category, CategoryCreate, CategoryUpdate
from domain.category.use_cases.get_category import GetCategoriesUseCase
from domain.category.use_cases.get_category_by_id import GetCategoryByIdUseCase
from domain.category.use_cases.create_category import CreateCategoryUseCase
from domain.category.use_cases.update_category import UpdateCategoryUseCase
from domain.category.use_cases.delete_category import DeleteCategoryUseCase
from core.exceptions.domain_exceptions import (
    CategoryNotFoundError, CategoryAlreadyExistsError
)

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=list[Category])
async def get_categories():
    return await GetCategoriesUseCase().execute()

@router.get("/{category_id}", response_model=Category)
async def get_category_by_id(category_id: int):
    try:
        return await GetCategoryByIdUseCase().execute(category_id=category_id)
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)

@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(category_data: CategoryCreate):
    try:
        return await CreateCategoryUseCase().execute(category_data=category_data)
    except CategoryAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=e.detail)

@router.put("/{category_id}", response_model=Category)
async def update_category(category_id: int, category_data: CategoryUpdate):
    try:
        return await UpdateCategoryUseCase().execute(category_id=category_id, category_data=category_data)
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except CategoryAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=e.detail)

@router.delete("/{category_id}")
async def delete_category(category_id: int):
    try:
        return await DeleteCategoryUseCase().execute(category_id=category_id)
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)