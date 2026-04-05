from fastapi import APIRouter
from app.services.park_service import ParkService
from app.schemas.park import ParkResponse

router = APIRouter()

@router.get('/', response_model=list[ParkResponse])
def get_parks():
    return ParkService.list_parks()
