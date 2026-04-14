from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.health_service import HealthService
from app.schemas.health import HealthProfileCreate, HealthProfileResponse, HealthAnalysisResponse, HealthHistoryResponse
from app.db import get_db
from app.repositories.user_repository import UserRepository

router = APIRouter()

# 🔹 OBTENER ANÁLISIS ESPECÍFICO (RUTA MÁS ESPECÍFICA - VA PRIMERO)
@router.get('/analysis/{analysis_id}', response_model=HealthAnalysisResponse)
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    """Obtiene los detalles completos de un análisis específico"""
    analysis = HealthService.get_analysis_by_id(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail='Análisis no encontrado')
    return analysis


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


# 🔹 GUARDAR / ACTUALIZAR PERFIL
@router.post('/{user_id}', response_model=HealthProfileResponse)
def save_profile(user_id: int, data: HealthProfileCreate, db: Session = Depends(get_db)):
    """Guardar o actualizar perfil de salud del usuario"""
    try:
        # Validar que el usuario existe
        user_exists = UserRepository.get_by_id(db, user_id) is not None
        if not user_exists:
            raise HTTPException(status_code=404, detail=f'Usuario {user_id} no existe')
        
        # Validar datos
        if data.height_cm <= 0 or data.weight_kg <= 0 or data.resting_hr < 0:
            raise HTTPException(status_code=400, detail='Los valores deben ser mayores a 0')
        
        if data.resting_hr > 200:
            raise HTTPException(status_code=400, detail='FC en reposo inválida (>200)')
        
        # Crear o actualizar profile - this handles both profile and analysis in one transaction
        profile = HealthService.create_or_update_profile(
            db,
            user_id,
            data.height_cm,
            data.weight_kg,
            data.resting_hr,
            data.age
        )
        
        # Explicit commit - all or nothing
        db.commit()
        db.refresh(profile)  # Refresh to get latest values after commit
        
        return profile
    except HTTPException:
        raise
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        print(f"Error saving health profile: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f'Error guardando perfil: {str(e)}')


# 🔹 OBTENER PERFIL ACTUAL (RUTA GENÉRICA - VA AL FINAL)
@router.get('/{user_id}', response_model=HealthProfileResponse)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = HealthService.get_profile(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail='Perfil de salud no encontrado')
    return profile


# 🔹 ELIMINAR PERFIL
@router.delete('/{user_id}')
def delete_profile(user_id: int, db: Session = Depends(get_db)):
    try:
        success = HealthService.delete_profile(db, user_id)
        if not success:
            raise HTTPException(status_code=404, detail='Perfil no encontrado')
        db.commit()
        return {"message": "Perfil de salud eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(exc))