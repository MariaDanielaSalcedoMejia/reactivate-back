from datetime import datetime
from typing import List

from sqlalchemy.orm import Session
from app.schemas.forum import ForumPostCreate
from app.repositories.forum_repository import ForumRepository
from app.repositories.user_repository import UserRepository


def format_time_ago(created_at: datetime) -> str:
    delta = datetime.utcnow() - created_at
    if delta.days >= 1:
        return f"{delta.days} día{'s' if delta.days != 1 else ''}"
    hours = delta.seconds // 3600
    if hours >= 1:
        return f"{hours} hora{'s' if hours != 1 else ''}"
    minutes = delta.seconds // 60
    if minutes >= 1:
        return f"{minutes} minuto{'s' if minutes != 1 else ''}"
    return 'Ahora mismo'


class ForumService:
    @staticmethod
    def list_categories(db: Session) -> List[dict]:
        categories = ForumRepository.list_categories(db)
        return [
            {
                'name': category.name,
                'description': category.description or '',
                'icon': category.icon or '',
                'posts': len(category.posts),
                'topics': len(category.posts)
            }
            for category in categories
        ]

    @staticmethod
    def list_posts(db: Session) -> List[dict]:
        posts = ForumRepository.list_posts(db)
        return [
            {
                'id': post.id,
                'title': post.title,
                'excerpt': post.excerpt or '',
                'author': post.author.name if post.author else 'Anónimo',
                'time_ago': format_time_ago(post.created_at),
                'category': post.category.name if post.category else 'Sin categoría',
                'likes': post.likes_count,
                'replies': post.replies_count
            }
            for post in posts
        ]

    @staticmethod
    def create_post(db: Session, data: ForumPostCreate) -> dict:
        category = ForumRepository.get_category_by_name(db, data.category)
        if category is None:
            category = ForumRepository.create_category(db, data.category, description='', icon='')

        author = None
        if '@' in data.author:
            author = UserRepository.get_by_email(db, data.author)
        else:
            author = UserRepository.get_by_name(db, data.author)

        forum_post = ForumRepository.create_post(
            db,
            title=data.title,
            content=data.content,
            excerpt=data.excerpt,
            author_id=author.id if author else None,
            category_id=category.id
        )

        return {
            'id': forum_post.id,
            'title': forum_post.title,
            'excerpt': forum_post.excerpt or '',
            'author': forum_post.author.name if forum_post.author else data.author,
            'category': category.name,
            'time_ago': format_time_ago(forum_post.created_at),
            'likes': forum_post.likes_count,
            'replies': forum_post.replies_count
        }
