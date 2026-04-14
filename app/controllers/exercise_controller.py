from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.exercise_service import ExerciseService
from app.schemas.exercise import ExerciseResponse, ExerciseCreate, ExerciseUpdate
from app.db import get_db

router = APIRouter()

@router.get('/', response_model=list[ExerciseResponse])
def get_exercises(db: Session = Depends(get_db)):
    return ExerciseService.list_exercises(db)

@router.post('/', response_model=ExerciseResponse)
def create_exercise(payload: ExerciseCreate, db: Session = Depends(get_db)):
    try:
        if not payload.nombre:
            raise HTTPException(status_code=400, detail='El nombre del ejercicio es obligatorio')
        exercise = ExerciseService.create_exercise(db, payload.nombre, payload.tipo, payload.descripcion, payload.imagen)
        db.commit()
        return exercise
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(exc))

@router.get('/{exercise_id}', response_model=ExerciseResponse)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = ExerciseService.get_exercise(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail='Ejercicio no encontrado')
    return exercise

@router.put('/{exercise_id}', response_model=ExerciseResponse)
def update_exercise(exercise_id: int, payload: ExerciseUpdate, db: Session = Depends(get_db)):
    try:
        exercise = ExerciseService.update_exercise(db, exercise_id, payload.nombre, payload.tipo, payload.descripcion, payload.imagen)
        if not exercise:
            raise HTTPException(status_code=404, detail='Ejercicio no encontrado')
        db.commit()
        return exercise
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(exc))

@router.delete('/{exercise_id}')
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    try:
        success = ExerciseService.delete_exercise(db, exercise_id)
        if not success:
            raise HTTPException(status_code=404, detail='Ejercicio no encontrado')
        db.commit()
        return {"message": "Ejercicio eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(exc))
