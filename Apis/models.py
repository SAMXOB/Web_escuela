from pydantic import BaseModel, Field
from typing import List, Optional

class Estudiante (BaseModel):
    id: int = Field(..., example=1)
    nombre: str = Field(..., example = "Ana")
    apellido: str = Field(..., example = "Gomez")
    email: str = Field(..., example = "ana@example.com")
    materias: Optional[List[int]] = Field(default=None, example = 1)

class Profesor(BaseModel):
    id: int = Field(..., example = 1)
    nombre: str = Field(..., example = "Carlos")
    apellido: str = Field(..., example = "Ruiz")
    email: str = Field(..., example = "carlos@example.com")
    materia_id: Optional[int] = Field(default=None, example=1)

class Materia(BaseModel):
    id: int = Field(..., example=1)
    nombre: str = Field(..., example="Matemáticas")
    creditos: int = Field(..., example=3)
    profesor_id: Optional[int] = Field(default=None, example=1)


