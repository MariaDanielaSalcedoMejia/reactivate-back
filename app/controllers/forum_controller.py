from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.forum import ForumCategoryResponse, ForumPostCreate, ForumPostResponse
from app.services.forum_service import ForumService
from app.db import get_db

router = APIRouter()

@router.get('/categories', response_model=list[ForumCategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return ForumService.list_categories(db)

@router.get('/posts', response_model=list[ForumPostResponse])
def list_posts(db: Session = Depends(get_db)):
    return ForumService.list_posts(db)

@router.post('/posts', response_model=ForumPostResponse)
def create_post(payload: ForumPostCreate, db: Session = Depends(get_db)):
    return ForumService.create_post(db, payload)
