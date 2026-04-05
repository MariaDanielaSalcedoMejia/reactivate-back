from sqlalchemy.orm import Session
from app.models.exercise import Exercise


class ExerciseRepository:
    @staticmethod
    def list_exercises(db: Session) -> list[Exercise]:
        return db.query(Exercise).order_by(Exercise.name).all()
