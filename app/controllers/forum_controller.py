from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.forum import ForumCategoryResponse, ForumPostCreate, ForumPostResponse, ForumCategoryCreate
from app.services.forum_service import ForumService
from app.db import get_db

router = APIRouter()

@router.get('/categories', response_model=list[ForumCategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return ForumService.list_categories(db)

@router.post('/categories', response_model=ForumCategoryResponse)
def create_category(payload: ForumCategoryCreate, db: Session = Depends(get_db)):
    return ForumService.create_category(db, payload.name, payload.description, payload.icon)

@router.get('/posts', response_model=list[ForumPostResponse])
def list_posts(db: Session = Depends(get_db)):
    return ForumService.list_posts(db)

@router.post('/posts', response_model=ForumPostResponse)
def create_post(payload: ForumPostCreate, db: Session = Depends(get_db)):
    if not payload.title or not payload.content:
        raise HTTPException(status_code=400, detail='El título y contenido son obligatorios')
    return ForumService.create_post(db, payload)

@router.get('/posts/{post_id}', response_model=ForumPostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = ForumService.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail='Post no encontrado')
    return post

@router.delete('/posts/{post_id}')
def delete_post(post_id: int, db: Session = Depends(get_db)):
    success = ForumService.delete_post(db, post_id)
    if not success:
        raise HTTPException(status_code=404, detail='Post no encontrado')
    return {"message": "Post eliminado correctamente"}
