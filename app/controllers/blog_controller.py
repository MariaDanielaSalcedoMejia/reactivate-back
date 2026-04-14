from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.blog import BlogPostCreate, BlogPostResponse, BlogPostUpdate
from app.services.blog_service import BlogService
from app.db import get_db

router = APIRouter()

@router.get('/posts', response_model=list[BlogPostResponse])
def list_posts(db: Session = Depends(get_db)):
    return BlogService.list_posts(db)

@router.post('/posts', response_model=BlogPostResponse)
def create_post(payload: BlogPostCreate, db: Session = Depends(get_db)):
    try:
        if not payload.title or not payload.content:
            raise HTTPException(status_code=400, detail='Título y contenido son obligatorios')
        post = BlogService.create_post(db, payload.title, payload.content, payload.author_email)
        db.commit()
        return post
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(exc))

@router.get('/posts/{post_id}', response_model=BlogPostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = BlogService.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail='Post no encontrado')
    return post

@router.put('/posts/{post_id}', response_model=BlogPostResponse)
def update_post(post_id: int, payload: BlogPostUpdate, db: Session = Depends(get_db)):
    try:
        post = BlogService.update_post(db, post_id, payload.title, payload.content)
        if not post:
            raise HTTPException(status_code=404, detail='Post no encontrado')
        db.commit()
        return post
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(exc))

@router.delete('/posts/{post_id}')
def delete_post(post_id: int, db: Session = Depends(get_db)):
    try:
        success = BlogService.delete_post(db, post_id)
        if not success:
            raise HTTPException(status_code=404, detail='Post no encontrado')
        db.commit()
        return {"message": "Post eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(exc))
