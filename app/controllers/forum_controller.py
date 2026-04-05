from fastapi import APIRouter
from app.schemas.forum import ForumCategoryResponse, ForumPostCreate, ForumPostResponse
from app.services.forum_service import ForumService

router = APIRouter()

@router.get('/categories', response_model=list[ForumCategoryResponse])
def list_categories():
    return ForumService.list_categories()

@router.get('/posts', response_model=list[ForumPostResponse])
def list_posts():
    return ForumService.list_posts()

@router.post('/posts', response_model=ForumPostResponse)
def create_post(payload: ForumPostCreate):
    return ForumService.create_post(payload)
