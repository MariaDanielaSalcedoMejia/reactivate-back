from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from .base import Base


class HealthAnalysis(Base):
    """
    Modelo para guardar histórico de análisis de salud
    Cada vez que el usuario se realiza un análisis, se crea un registro aquí
    """
    __tablename__ = 'health_analysis'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Datos biométricos
    height_cm = Column(Float, nullable=False)
    weight_kg = Column(Float, nullable=False)
    resting_hr = Column(Integer, nullable=False)
    age = Column(Integer, nullable=True)  # Edad en el momento del análisis
    
    # Métricas calculadas
    imc = Column(Float, nullable=False)
    imc_category = Column(String(50), nullable=False)  # Bajo peso, Óptimo, Sobrepeso, Obesidad
    
    # Score y recomendaciones
    score = Column(Integer, nullable=False)
    level = Column(String(100), nullable=False)
    recommendation = Column(Text, nullable=False)
    
    # Análisis adicionales
    max_hr = Column(Integer, nullable=True)  # Frecuencia cardíaca máxima (220 - edad)
    heart_reserve = Column(Integer, nullable=True)  # Reserva cardíaca (max_hr - resting_hr)
    
    # Zonas de ejercicio
    recovery_zone_min = Column(Integer, nullable=True)
    recovery_zone_max = Column(Integer, nullable=True)
    aerobic_zone_min = Column(Integer, nullable=True)
    aerobic_zone_max = Column(Integer, nullable=True)
    performance_zone_min = Column(Integer, nullable=True)
    performance_zone_max = Column(Integer, nullable=True)
    
    # Resumen de conclusiones
    health_summary = Column(Text, nullable=True)  # Resumen en texto
    warnings = Column(Text, nullable=True)  # Alertas importantes (JSON)
    suggestions = Column(Text, nullable=True)  # Sugerencias de mejora (JSON)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación
    user = relationship('User', backref='health_analysis_history')
