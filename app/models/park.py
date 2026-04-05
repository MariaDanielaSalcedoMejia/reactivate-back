from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from .base import Base

exercise_park = Table(
    'exercise_park',
    Base.metadata,
    Column('exercise_id', Integer, ForeignKey('exercises.id', ondelete='CASCADE'), primary_key=True),
    Column('park_id', Integer, ForeignKey('parks.id', ondelete='CASCADE'), primary_key=True)
)


class Park(Base):
    __tablename__ = 'parks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    address = Column(Text, nullable=True)
    rating = Column(Numeric(2, 1), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    features = relationship('ParkFeature', back_populates='park', cascade='all, delete-orphan')
    exercises = relationship('Exercise', secondary=exercise_park, back_populates='parks')


class ParkFeature(Base):
    __tablename__ = 'park_features'

    id = Column(Integer, primary_key=True, index=True)
    park_id = Column(Integer, ForeignKey('parks.id', ondelete='CASCADE'))
    name = Column(String(100), nullable=False)

    park = relationship('Park', back_populates='features')
