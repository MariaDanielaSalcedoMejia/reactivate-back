from pydantic import BaseModel

class ExerciseResponse(BaseModel):
    nombre: str
    tipo: str
    descripcion: str
    imagen: str
    parque: str
