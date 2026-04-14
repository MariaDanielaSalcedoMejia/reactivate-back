from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.health_service import HealthService
from app.schemas.health import HealthProfileCreate, HealthProfileResponse, HealthAnalysisResponse, HealthHistoryResponse
from app.db import get_db

router = APIRouter()

# 🔹 GUARDAR / ACTUALIZAR PERFIL
@router.post('/{user_id}', response_model=HealthProfileResponse)
def save_profile(user_id: int, data: HealthProfileCreate, db: Session = Depends(get_db)):
    try:
        if data.height_cm <= 0 or data.weight_kg <= 0 or data.resting_hr < 0:
            raise HTTPException(status_code=400, detail='Los valores deben ser mayores a 0')
        
        profile = HealthService.create_or_update_profile(
            db,
            user_id,
            data.height_cm,
            data.weight_kg,
            data.resting_hr,
            data.age
        )
        return profile
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 🔹 OBTENER PERFIL ACTUAL
@router.get('/{user_id}', response_model=HealthProfileResponse)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = HealthService.get_profile(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail='Perfil de salud no encontrado')
    return profile


# 🔹 OBTENER HISTORIAL COMPLETO DE ANÁLISIS
@router.get('/{user_id}/history', response_model=list[HealthAnalysisResponse])
def get_analysis_history(user_id: int, db: Session = Depends(get_db)):
    """Obtiene el historial completo de análisis de salud del usuario"""
    history = HealthService.get_analysis_history(db, user_id)
    if not history:
        return []
    return history


# 🔹 OBTENER HISTORIAL SIMPLIFICADO (PARA GRÁFICAS)
@router.get('/{user_id}/history-summary', response_model=list[HealthHistoryResponse])
def get_history_summary(user_id: int, db: Session = Depends(get_db)):
    """Obtiene un resumen del historial para gráficas y visualizaciones"""
    history = HealthService.get_analysis_history(db, user_id)
    if not history:
        return []
    return history


# 🔹 OBTENER ANÁLISIS ESPECÍFICO
@router.get('/analysis/{analysis_id}', response_model=HealthAnalysisResponse)
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    """Obtiene los detalles completos de un análisis específico"""
    analysis = HealthService.get_analysis_by_id(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail='Análisis no encontrado')
    return analysis


# 🔹 ELIMINAR PERFIL
@router.delete('/{user_id}')
def delete_profile(user_id: int, db: Session = Depends(get_db)):
    success = HealthService.delete_profile(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail='Perfil no encontrado')
    return {"message": "Perfil de salud eliminado correctamente"}