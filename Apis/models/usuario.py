from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from . import Base
from .audit_mixin import AuditMixin

class Usuario(Base, AuditMixin):
    __tablename__ = "usuarios"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
