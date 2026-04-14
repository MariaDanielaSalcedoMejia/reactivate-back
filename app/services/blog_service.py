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

    @staticmethod
    def get_post(db: Session, post_id: int) -> BlogPost | None:
        return BlogRepository.get_post(db, post_id)

    @staticmethod
    def update_post(db: Session, post_id: int, title: str | None, content: str | None) -> BlogPost | None:
        return BlogRepository.update_post(db, post_id, title, content)

    @staticmethod
    def delete_post(db: Session, post_id: int) -> bool:
        return BlogRepository.delete_post(db, post_id)
