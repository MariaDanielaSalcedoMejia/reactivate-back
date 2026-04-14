from pydantic import BaseModel
from datetime import datetime

class HealthProfileCreate(BaseModel):
    height_cm: float
    weight_kg: float
    resting_hr: int
    age: int | None = None

class HealthProfileResponse(BaseModel):
    user_id: int
    height_cm: float
    weight_kg: float
    resting_hr: int
    imc: float
    score: int
    level: str
    recommendation: str

    class Config:
        from_attributes = True


class HealthAnalysisResponse(BaseModel):
    id: int
    user_id: int
    height_cm: float
    weight_kg: float
    resting_hr: int
    age: int | None
    imc: float
    imc_category: str
    score: int
    level: str
    recommendation: str
    max_hr: int | None
    heart_reserve: int | None
    recovery_zone_min: int | None
    recovery_zone_max: int | None
    aerobic_zone_min: int | None
    aerobic_zone_max: int | None
    performance_zone_min: int | None
    performance_zone_max: int | None
    health_summary: str | None
    warnings: str | None
    suggestions: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class HealthHistoryResponse(BaseModel):
    """Respuesta simplificada para el histórico"""
    id: int
    created_at: datetime
    imc: float
    imc_category: str
    score: int
    level: str
    health_summary: str | None

    class Config:
        from_attributes = True

