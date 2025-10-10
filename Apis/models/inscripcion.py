import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from . import Base                   # ✅ cambio clave
from .audit_mixin import AuditMixin

class Inscripcion(Base, AuditMixin):
    __tablename__ = "inscripciones"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    estudiante_id = Column(UUID(as_uuid=True), ForeignKey("estudiantes.id", ondelete="CASCADE"))
    curso_id = Column(UUID(as_uuid=True), ForeignKey("cursos.id", ondelete="CASCADE"))

    estudiante = relationship("Estudiante", back_populates="inscripciones")
    curso = relationship("Curso", back_populates="inscripciones")
