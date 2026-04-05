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
        category = ForumCategory(name=name, description=description or '', icon=icon or '')
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def list_posts(db: Session) -> list[ForumPost]:
        return db.query(ForumPost).order_by(ForumPost.created_at.desc()).all()

    @staticmethod
    def create_post(db: Session, title: str, content: str, excerpt: str | None, author_id: int | None, category_id: int | None) -> ForumPost:
        post = ForumPost(
            title=title,
            content=content,
            excerpt=excerpt,
            author_id=author_id,
            category_id=category_id
        )
        db.add(post)
        db.commit()
        db.refresh(post)
        return post
