from pydantic import BaseModel

class ExerciseCreate(BaseModel):
    nombre: str
    tipo: str | None = None
    descripcion: str | None = None
    imagen: str | None = None

class ExerciseUpdate(BaseModel):
    nombre: str | None = None
    tipo: str | None = None
    descripcion: str | None = None
    imagen: str | None = None

class ExerciseResponse(BaseModel):
    nombre: str
    tipo: str | None = None
    descripcion: str | None = None
    imagen: str | None = None
    parque: str | None = None
