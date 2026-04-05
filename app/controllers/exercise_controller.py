from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.exercise_service import ExerciseService
from app.schemas.exercise import ExerciseResponse
from app.db import get_db

router = APIRouter()

@router.get('/', response_model=list[ExerciseResponse])
def get_exercises(db: Session = Depends(get_db)):
    return ExerciseService.list_exercises(db)
