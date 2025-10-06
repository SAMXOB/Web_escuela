from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from Apis.database import Base


class AuditMixin:
    creado_por = Column(String, nullable=False)
    actualizado_por = Column(String, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Usuario(Base, AuditMixin):
    __tablename__ = "usuarios"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


class Estudiante(Base, AuditMixin):
    __tablename__ = "estudiantes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    inscripciones = relationship("Inscripcion", back_populates="estudiante")


class Profesor(Base, AuditMixin):
    __tablename__ = "profesores"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    materias = relationship("Materia", back_populates="profesor")


class Materia(Base, AuditMixin):
    __tablename__ = "materias"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False)
    creditos = Column(Integer, nullable=False)

    profesor_id = Column(UUID(as_uuid=True), ForeignKey("profesores.id"))
    profesor = relationship("Profesor", back_populates="materias")

    cursos = relationship("Curso", back_populates="materia")


class Curso(Base, AuditMixin):
    __tablename__ = "cursos"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False)

    materia_id = Column(UUID(as_uuid=True), ForeignKey("materias.id"))
    materia = relationship("Materia", back_populates="cursos")

    inscripciones = relationship("Inscripcion", back_populates="curso")


class Inscripcion(Base, AuditMixin):
    __tablename__ = "inscripciones"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    estudiante_id = Column(UUID(as_uuid=True), ForeignKey("estudiantes.id"))
    curso_id = Column(UUID(as_uuid=True), ForeignKey("cursos.id"))

    estudiante = relationship("Estudiante", back_populates="inscripciones")
    curso = relationship("Curso", back_populates="inscripciones")
