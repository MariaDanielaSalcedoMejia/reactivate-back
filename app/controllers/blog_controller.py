from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.blog import BlogPostCreate, BlogPostResponse
from app.services.blog_service import BlogService
from app.db import get_db

router = APIRouter()

@router.get('/posts', response_model=list[BlogPostResponse])
def list_posts(db: Session = Depends(get_db)):
    return BlogService.list_posts(db)

@router.post('/posts', response_model=BlogPostResponse)
def create_post(payload: BlogPostCreate, db: Session = Depends(get_db)):
    if not payload.title or not payload.content:
        raise HTTPException(status_code=400, detail='Título y contenido son obligatorios')
    return BlogService.create_post(db, payload.title, payload.content, payload.author_email)
