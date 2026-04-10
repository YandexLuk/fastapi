from fastapi import APIRouter, status, HTTPException
from schemas.location import Location, LocationCreate, LocationUpdate
from domain.location.use_cases.get_location import GetLocationsUseCase
from domain.location.use_cases.get_location_id import GetLocationByIdUseCase
from domain.location.use_cases.create_location import CreateLocationUseCase
from domain.location.use_cases.update_location import UpdateLocationUseCase
from domain.location.use_cases.delete_location import DeleteLocationUseCase
from core.exceptions.domain_exceptions import (
    LocationNotFoundError, LocationAlreadyExistsError
)

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.get("/", response_model=list[Location])
async def get_locations():
    return await GetLocationsUseCase().execute()

@router.get("/{location_id}", response_model=Location)
async def get_location_by_id(location_id: int):
    try:
        return await GetLocationByIdUseCase().execute(location_id=location_id)
    except LocationNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)

@router.post("/", response_model=Location, status_code=status.HTTP_201_CREATED)
async def create_location(location_data: LocationCreate):
    try:
        return await CreateLocationUseCase().execute(location_data=location_data)
    except LocationAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=e.detail)

@router.put("/{location_id}", response_model=Location)
async def update_location(location_id: int, location_data: LocationUpdate):
    try:
        return await UpdateLocationUseCase().execute(location_id=location_id, location_data=location_data)
    except LocationNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except LocationAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=e.detail)

@router.delete("/{location_id}")
async def delete_location(location_id: int):
    try:
        return await DeleteLocationUseCase().execute(location_id=location_id)
    except LocationNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)