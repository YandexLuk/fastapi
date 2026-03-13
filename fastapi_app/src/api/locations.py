from fastapi import APIRouter, status, HTTPException

from schemas.location import Location, LocationCreate, LocationUpdate
from domain.location.use_cases.get_location import GetLocationsUseCase
from domain.location.use_cases.get_location_id import GetLocationByIdUseCase
from domain.location.use_cases.create_location import CreateLocationUseCase
from domain.location.use_cases.update_location import UpdateLocationUseCase
from domain.location.use_cases.delete_location import DeleteLocationUseCase

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/", response_model=list[Location], status_code=status.HTTP_200_OK)
async def get_locations():
    use_case = GetLocationsUseCase()
    return await use_case.execute()


@router.get("/{location_id}", response_model=Location, status_code=status.HTTP_200_OK)
async def get_location_by_id(location_id: int):
    use_case = GetLocationByIdUseCase()
    location = await use_case.execute(location_id=location_id)
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    return location


@router.post("/", response_model=Location, status_code=status.HTTP_201_CREATED)
async def create_location(location_data: LocationCreate):
    use_case = CreateLocationUseCase()
    return await use_case.execute(location_data=location_data)


@router.put("/{location_id}", response_model=Location, status_code=status.HTTP_200_OK)
async def update_location(location_id: int, location_data: LocationUpdate):
    use_case = UpdateLocationUseCase()
    location = await use_case.execute(location_id=location_id, location_data=location_data)
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    return location


@router.delete("/{location_id}", status_code=status.HTTP_200_OK)
async def delete_location(location_id: int):
    use_case = DeleteLocationUseCase()
    result = await use_case.execute(location_id=location_id)
    if not result["deleted"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    return result