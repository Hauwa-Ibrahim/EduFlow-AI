from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine

# ==========================================================
# Models
# ==========================================================

from app.models.student import Student
from app.models.application import LoanApplication
from app.models.document import Document
from app.models.user import User
from app.models.audit_log import AuditLog
from app.models.notification import Notification

# ==========================================================
# Routers
# ==========================================================

from app.routers.home import router as home_router
from app.routers.auth import router as auth_router
from app.routers.students import router as students_router
from app.routers.applications import router as applications_router
from app.routers.documents import router as documents_router
from app.routers.fraud import router as fraud_router
from app.routers.dashboard import router as dashboard_router
from app.routers.audit import router as audit_router
from app.routers.notifications import router as notifications_router

# ==========================================================
# Create Database Tables
# ==========================================================

Base.metadata.create_all(bind=engine)

# ==========================================================
# FastAPI App
# ==========================================================

app = FastAPI(
    title="EduFlow AI Student Services Platform",
    description="An enterprise AI-powered platform for managing student loan applications.",
    version="1.0.0",
)

# ==========================================================
# CORS Configuration
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# Register Routers
# ==========================================================

app.include_router(home_router)
app.include_router(auth_router)
app.include_router(students_router)
app.include_router(applications_router)
app.include_router(documents_router)
app.include_router(fraud_router)
app.include_router(dashboard_router)
app.include_router(audit_router)
app.include_router(notifications_router)