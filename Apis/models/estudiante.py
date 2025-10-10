import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from . import Base                    # ✅ cambio clave
from .audit_mixin import AuditMixin

class Estudiante(Base, AuditMixin):
    __tablename__ = "estudiantes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)

    inscripciones = relationship(
        "Inscripcion",
        back_populates="estudiante",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
