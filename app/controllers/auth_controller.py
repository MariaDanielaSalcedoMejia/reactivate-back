from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import RegisterRequest, LoginRequest, UserResponse
from app.services.auth_service import AuthService
from app.db import get_db

router = APIRouter()

@router.post('/register', response_model=UserResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = AuthService.register(db, payload.name, payload.email, payload.password, payload.birth_date)
        return user
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.post('/login', response_model=UserResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = AuthService.login(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail='Credenciales inválidas')
    return user

@router.get('/me', response_model=UserResponse)
def me(email: str, db: Session = Depends(get_db)):
    user = AuthService.get_user(db, email)
    if not user:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return user
