from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    application_id = Column(
        Integer,
        nullable=False,
    )

    action = Column(
        String,
        nullable=False,
    )

    performed_by = Column(
        String,
        nullable=False,
    )

    details = Column(
        String,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )