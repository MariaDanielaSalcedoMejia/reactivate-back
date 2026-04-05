from pydantic import BaseModel

class HealthProfileCreate(BaseModel):
    height_cm: float
    weight_kg: float
    resting_hr: int

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
        orm_mode = True
