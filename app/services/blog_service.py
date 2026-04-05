from sqlalchemy.orm import Session
from app.repositories.blog_repository import BlogRepository
from app.repositories.user_repository import UserRepository
from app.models.blog import BlogPost

class BlogService:
    @staticmethod
    def list_posts(db: Session) -> list[BlogPost]:
        return BlogRepository.list_posts(db)

    @staticmethod
    def create_post(db: Session, title: str, content: str, author_email: str) -> BlogPost:
        user = UserRepository.get_by_email(db, author_email)
        author_id = user.id if user else None
        return BlogRepository.create_post(db, title, content, author_id)
