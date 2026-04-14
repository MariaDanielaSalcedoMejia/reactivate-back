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

    @staticmethod
    def get_exercise(db: Session, exercise_id: int) -> dict | None:
        exercise = ExerciseRepository.get_exercise(db, exercise_id)
        if not exercise:
            return None
        return {
            "nombre": exercise.name,
            "tipo": exercise.type or "",
            "descripcion": exercise.description or "",
            "imagen": exercise.image or "",
            "parque": exercise.parks[0].name if exercise.parks else ""
        }

    @staticmethod
    def create_exercise(db: Session, nombre: str, tipo: str | None, descripcion: str | None, imagen: str | None) -> dict:
        exercise = ExerciseRepository.create_exercise(db, nombre, tipo, descripcion, imagen)
        return {
            "nombre": exercise.name,
            "tipo": exercise.type or "",
            "descripcion": exercise.description or "",
            "imagen": exercise.image or "",
            "parque": ""
        }

    @staticmethod
    def update_exercise(db: Session, exercise_id: int, nombre: str | None, tipo: str | None, descripcion: str | None, imagen: str | None) -> dict | None:
        exercise = ExerciseRepository.update_exercise(db, exercise_id, nombre, tipo, descripcion, imagen)
        if not exercise:
            return None
        return {
            "nombre": exercise.name,
            "tipo": exercise.type or "",
            "descripcion": exercise.description or "",
            "imagen": exercise.image or "",
            "parque": exercise.parks[0].name if exercise.parks else ""
        }

    @staticmethod
    def delete_exercise(db: Session, exercise_id: int) -> bool:
        return ExerciseRepository.delete_exercise(db, exercise_id)
