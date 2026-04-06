from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.health_service import HealthService
from app.schemas.health import HealthProfileCreate, HealthProfileResponse
from app.db import get_db

router = APIRouter()

# 🔹 GUARDAR / ACTUALIZAR PERFIL
@router.post('/{user_id}', response_model=HealthProfileResponse)
def save_profile(user_id: int, data: HealthProfileCreate, db: Session = Depends(get_db)):
    try:
        profile = HealthService.create_or_update_profile(
            db,
            user_id,
            data.height_cm,
            data.weight_kg,
            data.resting_hr
        )
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 🔹 OBTENER PERFIL
@router.get('/{user_id}', response_model=HealthProfileResponse | None)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = HealthService.get_profile(db, user_id)
    return profile