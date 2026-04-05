from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base


class ForumCategory(Base):
    __tablename__ = 'forum_categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    posts = relationship('ForumPost', back_populates='category')


class ForumPost(Base):
    __tablename__ = 'forum_posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    excerpt = Column(Text, nullable=True)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    category_id = Column(Integer, ForeignKey('forum_categories.id'), nullable=True)
    likes_count = Column(Integer, default=0)
    replies_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = relationship('User', backref='forum_posts')
    category = relationship('ForumCategory', back_populates='posts')
    comments = relationship('ForumComment', back_populates='post', cascade='all, delete-orphan')
    likes = relationship('Like', back_populates='post', cascade='all, delete-orphan')


class ForumComment(Base):
    __tablename__ = 'forum_comments'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    post_id = Column(Integer, ForeignKey('forum_posts.id', ondelete='CASCADE'))
    likes_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = relationship('User', back_populates='forum_comments')
    post = relationship('ForumPost', back_populates='comments')
    likes = relationship('Like', back_populates='comment', cascade='all, delete-orphan')


class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(Integer, ForeignKey('forum_posts.id', ondelete='CASCADE'), nullable=True)
    comment_id = Column(Integer, ForeignKey('forum_comments.id', ondelete='CASCADE'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', backref='likes')
    post = relationship('ForumPost', back_populates='likes')
    comment = relationship('ForumComment', back_populates='likes')

    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', 'comment_id', name='unique_like'),
    )
