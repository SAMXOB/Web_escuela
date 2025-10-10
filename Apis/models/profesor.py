import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from . import Base                # ✅ cambio aquí
from .audit_mixin import AuditMixin

class Profesor(Base, AuditMixin):
    __tablename__ = "profesores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)

    materias = relationship(
        "Materia",
        back_populates="profesor",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
