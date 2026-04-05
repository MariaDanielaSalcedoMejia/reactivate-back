from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class HealthProfile(Base):
    __tablename__ = 'health_profiles'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    height_cm = Column(Float, nullable=False)
    weight_kg = Column(Float, nullable=False)
    resting_hr = Column(Integer, nullable=False)
    imc = Column(Float, nullable=False)
    score = Column(Integer, nullable=False)
    level = Column(String(100), nullable=False)
    recommendation = Column(String(500), nullable=False)

    user = relationship('User', backref='health_profile')
