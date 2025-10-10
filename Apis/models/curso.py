import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from . import Base                    # ✅ cambio clave aquí
from .audit_mixin import AuditMixin

class Curso(Base, AuditMixin):
    __tablename__ = "cursos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False)

    materia_id = Column(UUID(as_uuid=True), ForeignKey("materias.id", ondelete="CASCADE"))
    materia = relationship("Materia", back_populates="cursos")

    inscripciones = relationship(
        "Inscripcion",
        back_populates="curso",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
