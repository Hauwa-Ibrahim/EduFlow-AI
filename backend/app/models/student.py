from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    institution = Column(String)
    programme = Column(String)
    status = Column(String, default="Pending")
    applications = relationship(
    "LoanApplication",
    back_populates="student"
)