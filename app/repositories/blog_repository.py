from sqlalchemy.orm import Session
from app.models.blog import BlogPost

class BlogRepository:
    @staticmethod
    def list_posts(db: Session) -> list[BlogPost]:
        return db.query(BlogPost).order_by(BlogPost.created_at.desc()).all()

    @staticmethod
    def get_post(db: Session, post_id: int) -> BlogPost | None:
        return db.query(BlogPost).filter(BlogPost.id == post_id).first()

    @staticmethod
    def create_post(db: Session, title: str, content: str, author_id: int | None = None) -> BlogPost:
        """Create post. Caller is responsible for commit."""
        post = BlogPost(title=title, content=content, author_id=author_id)
        db.add(post)
        return post

    @staticmethod
    def update_post(db: Session, post_id: int, title: str | None, content: str | None) -> BlogPost | None:
        """Update post. Caller is responsible for commit."""
        post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
        if not post:
            return None
        if title:
            post.title = title
        if content:
            post.content = content
        return post

    @staticmethod
    def delete_post(db: Session, post_id: int) -> bool:
        """Delete post. Caller is responsible for commit."""
        post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
        if not post:
            return False
        db.delete(post)
        return True
