from pydantic import BaseModel
from datetime import datetime

class BlogPostCreate(BaseModel):
    title: str
    content: str
    author_email: str

class BlogPostResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    author_id: int | None

    class Config:
        from_attributes = True
