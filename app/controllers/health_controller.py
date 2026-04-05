from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.health_service import HealthService
from app.schemas.health import HealthProfileCreate, HealthProfileResponse
from app.db import get_db

router = APIRouter()

@router.get('/{user_id}', response_model=HealthProfileResponse)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = HealthService.get_profile(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail='Perfil de salud no encontrado')
    return profile

@router.post('/{user_id}', response_model=HealthProfileResponse)
def create_or_update_profile(user_id: int, payload: HealthProfileCreate, db: Session = Depends(get_db)):
    return HealthService.create_or_update_profile(db, user_id, payload.height_cm, payload.weight_kg, payload.resting_hr)
