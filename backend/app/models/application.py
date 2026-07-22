from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship

from app.database.database import Base


class LoanApplication(Base):

    __tablename__ = "loan_applications"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False,
    )

    loan_type = Column(
        String,
        nullable=False,
    )

    academic_session = Column(
        String,
        nullable=False,
    )

    amount_requested = Column(
        Integer,
        nullable=False,
    )

    status = Column(
        String,
        default="Pending",
    )

    # ==========================================================
    # AI Decision Fields
    # ==========================================================

    eligibility_score = Column(
        Integer,
        default=0,
    )

    recommendation = Column(
        String,
        default="Pending",
    )

    risk_level = Column(
        String,
        default="Unknown",
    )

    ai_confidence = Column(
        Integer,
        default=0,
    )

    verification_status = Column(
        String,
        default="Pending",
    )

    # ==========================================================
    # Officer Review Fields
    # ==========================================================

    officer_decision = Column(
        String,
        nullable=True,
    )

    officer_comment = Column(
        String,
        nullable=True,
    )

    reviewed_by = Column(
        String,
        nullable=True,
    )

    reviewed_at = Column(
        DateTime,
        nullable=True,
    )

    # ==========================================================
    # Relationships
    # ==========================================================

    student = relationship(
        "Student",
        back_populates="applications",
    )

    documents = relationship(
        "Document",
        back_populates="application",
        cascade="all, delete",
    )