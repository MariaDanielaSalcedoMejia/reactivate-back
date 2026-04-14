from pydantic import BaseModel
from typing import List

class ParkCreate(BaseModel):
    name: str
    address: str | None = None
    rating: float | None = None

class ParkUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    rating: float | None = None

class ParkResponse(BaseModel):
    name: str
    address: str
    rating: float
    distance: str
    features: List[str]

class ExerciseResponse(BaseModel):
    nombre: str
    tipo: str
    descripcion: str
    imagen: str
    parque: str
