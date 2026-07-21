from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    application_id = Column(
        Integer,
        ForeignKey("loan_applications.id"),
        nullable=False,
    )

    document_type = Column(String, nullable=False)

    file_name = Column(String, nullable=False)

    file_path = Column(String, nullable=False)

    verification_status = Column(
        String,
        default="Pending",
    )

    confidence_score = Column(
        Integer,
        default=0,
    )

    matched_fields = Column(
        Text,
        nullable=True,
    )

    mismatched_fields = Column(
        Text,
        nullable=True,
    )

    application = relationship(
        "LoanApplication",
        back_populates="documents",
    )