from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    loan_type = Column(String, nullable=False)
    academic_session = Column(String, nullable=False)
    amount_requested = Column(Integer, nullable=False)

    status = Column(String, default="Pending")

    student = relationship("Student", back_populates="applications")