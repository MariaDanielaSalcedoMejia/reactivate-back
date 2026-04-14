from datetime import date

from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:
    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_name(db: Session, name: str) -> User | None:
        return db.query(User).filter(User.name == name).first()

    @staticmethod
    def create(db: Session, name: str, email: str, password_hash: str, birth_date: date | None = None, role: str = 'user') -> User:
        user = User(
            name=name,
            email=email,
            password_hash=password_hash,
            birth_date=birth_date,
            role=role
        )
        db.add(user)
        db.flush()  # Flush to assign ID
        db.refresh(user)  # Refresh to get all fields from DB
        return user
