from fastapi import APIRouter
from app.services.exercise_service import ExerciseService
from app.schemas.exercise import ExerciseResponse

router = APIRouter()

@router.get('/', response_model=list[ExerciseResponse])
def get_exercises():
    return ExerciseService.list_exercises()
