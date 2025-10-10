import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from . import Base
from .audit_mixin import AuditMixin

class Materia(Base, AuditMixin):
    __tablename__ = "materias"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False)
    creditos = Column(Integer, nullable=False)

    profesor_id = Column(UUID(as_uuid=True), ForeignKey("profesores.id", ondelete="SET NULL"), nullable=True)
    profesor = relationship("Profesor", back_populates="materias")

    cursos = relationship(
        "Curso",
        back_populates="materia",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
