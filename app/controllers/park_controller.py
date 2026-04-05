from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.park_service import ParkService
from app.schemas.park import ParkResponse
from app.db import get_db

router = APIRouter()

@router.get('/', response_model=list[ParkResponse])
def get_parks(db: Session = Depends(get_db)):
    return ParkService.list_parks(db)
