from typing import List
from sqlalchemy.orm import Session
from app.repositories.exercise_repository import ExerciseRepository


class ExerciseService:
    @staticmethod
    def list_exercises(db: Session) -> List[dict]:
        exercises = ExerciseRepository.list_exercises(db)
        return [
            {
                "nombre": exercise.name,
                "tipo": exercise.type or "",
                "descripcion": exercise.description or "",
                "imagen": exercise.image or "",
                "parque": exercise.parks[0].name if exercise.parks else ""
            }
            for exercise in exercises
        ]
