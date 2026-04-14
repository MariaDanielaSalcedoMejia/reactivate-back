from sqlalchemy.orm import Session
from app.models.exercise import Exercise


class ExerciseRepository:
    @staticmethod
    def list_exercises(db: Session) -> list[Exercise]:
        return db.query(Exercise).order_by(Exercise.name).all()

    @staticmethod
    def get_exercise(db: Session, exercise_id: int) -> Exercise | None:
        return db.query(Exercise).filter(Exercise.id == exercise_id).first()

    @staticmethod
    def create_exercise(db: Session, nombre: str, tipo: str | None, descripcion: str | None, imagen: str | None) -> Exercise:
        exercise = Exercise(name=nombre, type=tipo, description=descripcion, image=imagen)
        db.add(exercise)
        db.commit()
        db.refresh(exercise)
        return exercise

    @staticmethod
    def update_exercise(db: Session, exercise_id: int, nombre: str | None, tipo: str | None, descripcion: str | None, imagen: str | None) -> Exercise | None:
        exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if not exercise:
            return None
        if nombre:
            exercise.name = nombre
        if tipo:
            exercise.type = tipo
        if descripcion:
            exercise.description = descripcion
        if imagen:
            exercise.image = imagen
        db.commit()
        db.refresh(exercise)
        return exercise

    @staticmethod
    def delete_exercise(db: Session, exercise_id: int) -> bool:
        exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if not exercise:
            return False
        db.delete(exercise)
        db.commit()
        return True
