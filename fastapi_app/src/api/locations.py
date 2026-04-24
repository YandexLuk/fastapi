from fastapi import APIRouter, status, HTTPException, Depends
from schemas.location import Location, LocationCreate, LocationUpdate
from domain.location.use_cases.get_location import GetLocationsUseCase
from domain.location.use_cases.get_location_id import GetLocationByIdUseCase
from domain.location.use_cases.create_location import CreateLocationUseCase
from domain.location.use_cases.update_location import UpdateLocationUseCase
from domain.location.use_cases.delete_location import DeleteLocationUseCase
from core.exceptions.domain_exceptions import (
    LocationNotFoundError, LocationAlreadyExistsError
)
from core.dependencies import get_current_admin_user
from core.logging_config import get_logger

logger = get_logger("locations")

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/", response_model=list[Location])
async def get_locations():
    """Получить все локации. Публичный доступ."""
    return await GetLocationsUseCase().execute()


@router.get("/{location_id}", response_model=Location)
async def get_location_by_id(location_id: int):
    """Получить локацию по ID. Публичный доступ."""
    try:
        return await GetLocationByIdUseCase().execute(location_id=location_id)
    except LocationNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)


@router.post("/", response_model=Location, status_code=status.HTTP_201_CREATED)
async def create_location(location_data: LocationCreate, current_user=Depends(get_current_admin_user)):
    """Создать локацию. Только для администраторов."""
    try:
        result = await CreateLocationUseCase().execute(location_data=location_data)
        logger.info("Админ '%s' создал локацию '%s' (id=%s)", current_user.username, result.name, result.id)
        return result
    except LocationAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=e.detail)


@router.put("/{location_id}", response_model=Location)
async def update_location(location_id: int, location_data: LocationUpdate, current_user=Depends(get_current_admin_user)):
    """Обновить локацию. Только для администраторов."""
    try:
        result = await UpdateLocationUseCase().execute(location_id=location_id, location_data=location_data)
        logger.info("Админ '%s' обновил локацию (id=%s)", current_user.username, location_id)
        return result
    except LocationNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except LocationAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=e.detail)


@router.delete("/{location_id}")
async def delete_location(location_id: int, current_user=Depends(get_current_admin_user)):
    """Удалить локацию. Только для администраторов."""
    try:
        result = await DeleteLocationUseCase().execute(location_id=location_id)
        logger.info("Админ '%s' удалил локацию (id=%s)", current_user.username, location_id)
        return result
    except LocationNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)