from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from uuid import UUID

# ------------------ USUARIO ------------------ #
class UsuarioBase(BaseModel):
    username: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioResponse(UsuarioBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

# ------------------ ESTUDIANTE ------------------ #
class EstudianteBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr

class EstudianteCreate(EstudianteBase):
    pass

class EstudianteResponse(EstudianteBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

# ------------------ PROFESOR ------------------ #
class ProfesorBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr

class ProfesorCreate(ProfesorBase):
    pass

class ProfesorResponse(ProfesorBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

# ------------------ MATERIA ------------------ #
class MateriaBase(BaseModel):
    nombre: str
    creditos: int

class MateriaCreate(MateriaBase):
    profesor_id: UUID

class MateriaResponse(MateriaBase):
    id: UUID
    profesor_id: UUID
    model_config = ConfigDict(from_attributes=True)

# ------------------ CURSO ------------------ #
class CursoBase(BaseModel):
    nombre: str

class CursoCreate(CursoBase):
    materia_id: UUID

class CursoResponse(CursoBase):
    id: UUID
    materia_id: UUID
    model_config = ConfigDict(from_attributes=True)

# ------------------ INSCRIPCION ------------------ #
class InscripcionBase(BaseModel):
    estudiante_id: UUID
    curso_id: UUID

class InscripcionCreate(InscripcionBase):
    pass

class InscripcionResponse(InscripcionBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
