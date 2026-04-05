from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.models.user import User
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return pwd_context.verify(password, password_hash)

    @staticmethod
    def register(db: Session, name: str, age: int, email: str, password: str) -> User:
        existing = UserRepository.get_by_email(db, email)
        if existing:
            raise ValueError('El correo ya está registrado')

        password_hash = AuthService.hash_password(password)
        return UserRepository.create(db, name, age, email, password_hash)

    @staticmethod
    def login(db: Session, email: str, password: str) -> User | None:
        user = UserRepository.get_by_email(db, email)
        if not user:
            return None
        if not AuthService.verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def get_user(db: Session, email: str) -> Optional[User]:
        return UserRepository.get_by_email(db, email)
