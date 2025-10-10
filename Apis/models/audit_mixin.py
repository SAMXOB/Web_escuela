from datetime import datetime
from sqlalchemy import Column, DateTime, String


class AuditMixin:
    creado_por = Column(String, nullable=False)
    actualizado_por = Column(String, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)