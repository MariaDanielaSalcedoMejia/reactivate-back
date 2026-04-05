from sqlalchemy.orm import Session
from app.models.blog import BlogPost

class BlogRepository:
    @staticmethod
    def list_posts(db: Session) -> list[BlogPost]:
        return db.query(BlogPost).order_by(BlogPost.created_at.desc()).all()

    @staticmethod
    def create_post(db: Session, title: str, content: str, author_id: int | None = None) -> BlogPost:
        post = BlogPost(title=title, content=content, author_id=author_id)
        db.add(post)
        db.commit()
        db.refresh(post)
        return post
