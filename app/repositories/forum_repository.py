from sqlalchemy.orm import Session
from app.models.forum import ForumCategory, ForumPost


class ForumRepository:
    @staticmethod
    def list_categories(db: Session) -> list[ForumCategory]:
        return db.query(ForumCategory).order_by(ForumCategory.name).all()

    @staticmethod
    def get_category_by_name(db: Session, name: str) -> ForumCategory | None:
        return db.query(ForumCategory).filter(ForumCategory.name == name).first()

    @staticmethod
    def create_category(db: Session, name: str, description: str | None = None, icon: str | None = None) -> ForumCategory:
        """Create category. Caller is responsible for commit."""
        category = ForumCategory(name=name, description=description or '', icon=icon or '')
        db.add(category)
        return category

    @staticmethod
    def list_posts(db: Session) -> list[ForumPost]:
        return db.query(ForumPost).order_by(ForumPost.created_at.desc()).all()

    @staticmethod
    def get_post(db: Session, post_id: int) -> ForumPost | None:
        return db.query(ForumPost).filter(ForumPost.id == post_id).first()

    @staticmethod
    def create_post(db: Session, title: str, content: str, excerpt: str | None, author_id: int | None, category_id: int | None) -> ForumPost:
        """Create post. Caller is responsible for commit."""
        post = ForumPost(
            title=title,
            content=content,
            excerpt=excerpt,
            author_id=author_id,
            category_id=category_id
        )
        db.add(post)
        return post

    @staticmethod
    def delete_post(db: Session, post_id: int) -> bool:
        """Delete post. Caller is responsible for commit."""
        post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
        if not post:
            return False
        db.delete(post)
        return True
