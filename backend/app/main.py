from fastapi import FastAPI

from app.database.database import Base, engine

from app.models.student import Student
from app.models.application import LoanApplication
from app.models.document import Document

from app.routers.home import router as home_router
from app.routers.students import router as students_router
from app.routers.applications import router as applications_router
from app.routers.documents import router as documents_router

# Create all database tables
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EduFlow AI Student Services Platform",
    description="An enterprise AI-powered platform for managing student loan applications.",
    version="1.0.0"
)

app.include_router(home_router)
app.include_router(students_router)
app.include_router(applications_router)
app.include_router(documents_router)