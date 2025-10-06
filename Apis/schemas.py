from pydantic import BaseModel, EmailStr
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

    class Config:
        orm_mode = True


# ------------------ ESTUDIANTE ------------------ #
class EstudianteBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr


class EstudianteCreate(EstudianteBase):
    pass


class EstudianteResponse(EstudianteBase):
    id: UUID

    class Config:
        orm_mode = True


# ------------------ PROFESOR ------------------ #
class ProfesorBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr


class ProfesorCreate(ProfesorBase):
    pass


class ProfesorResponse(ProfesorBase):
    id: UUID

    class Config:
        orm_mode = True


# ------------------ MATERIA ------------------ #
class MateriaBase(BaseModel):
    nombre: str
    creditos: int


class MateriaCreate(MateriaBase):
    profesor_id: UUID


class MateriaResponse(MateriaBase):
    id: UUID
    profesor_id: UUID

    class Config:
        orm_mode = True


# ------------------ CURSO ------------------ #
class CursoBase(BaseModel):
    nombre: str


class CursoCreate(CursoBase):
    materia_id: UUID


class CursoResponse(CursoBase):
    id: UUID
    materia_id: UUID

    class Config:
        orm_mode = True


# ------------------ INSCRIPCION ------------------ #
class InscripcionBase(BaseModel):
    estudiante_id: UUID
    curso_id: UUID


class InscripcionCreate(InscripcionBase):
    pass


class InscripcionResponse(InscripcionBase):
    id: UUID

    class Config:
        orm_mode = True
