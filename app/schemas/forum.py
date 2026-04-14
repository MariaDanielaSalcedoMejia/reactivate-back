from pydantic import BaseModel

class ForumCategoryCreate(BaseModel):
    name: str
    description: str | None = None
    icon: str | None = None

class ForumCategoryResponse(BaseModel):
    name: str
    description: str
    icon: str
    posts: int
    topics: int

class ForumPostCreate(BaseModel):
    title: str
    excerpt: str
    author: str
    category: str
    content: str

class ForumPostResponse(BaseModel):
    id: int
    title: str
    excerpt: str
    author: str
    category: str
    time_ago: str
    likes: int
    replies: int

    class Config:
        from_attributes = True
