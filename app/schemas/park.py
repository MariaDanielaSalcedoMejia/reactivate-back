from pydantic import BaseModel
from typing import List

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
