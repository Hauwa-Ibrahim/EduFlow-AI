from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.application import LoanApplication
from app.models.student import Student
from app.schemas.application import (
    LoanApplicationCreate,
    LoanApplicationResponse,
)

from app.schemas.status import StatusUpdate
router = APIRouter(
    prefix="/applications",
    tags=["Loan Applications"]
)


@router.get("/", response_model=list[LoanApplicationResponse])
def get_applications(db: Session = Depends(get_db)):
    return db.query(LoanApplication).all()


@router.post("/", response_model=LoanApplicationResponse)
def create_application(
    application: LoanApplicationCreate,
    db: Session = Depends(get_db),
):
    student = (
        db.query(Student)
        .filter(Student.id == application.student_id)
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student does not exist"
        )

    existing_application = (
        db.query(LoanApplication)
        .filter(
            LoanApplication.student_id == application.student_id,
            LoanApplication.academic_session == application.academic_session,
        )
        .first()
    )

    if existing_application:
        raise HTTPException(
            status_code=400,
            detail="Student has already applied for this academic session"
        )

    new_application = LoanApplication(
        student_id=application.student_id,
        loan_type=application.loan_type,
        academic_session=application.academic_session,
        amount_requested=application.amount_requested,
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


@router.get("/{application_id}", response_model=LoanApplicationResponse)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = (
        db.query(LoanApplication)
        .filter(LoanApplication.id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Loan application not found"
        )

    return application


@router.put("/{application_id}", response_model=LoanApplicationResponse)
def update_application(
    application_id: int,
    updated_application: LoanApplicationCreate,
    db: Session = Depends(get_db),
):
    application = (
        db.query(LoanApplication)
        .filter(LoanApplication.id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Loan application not found"
        )

    student = (
        db.query(Student)
        .filter(Student.id == updated_application.student_id)
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student does not exist"
        )

    application.student_id = updated_application.student_id
    application.loan_type = updated_application.loan_type
    application.academic_session = updated_application.academic_session
    application.amount_requested = updated_application.amount_requested

    db.commit()
    db.refresh(application)

    return application


@router.delete("/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = (
        db.query(LoanApplication)
        .filter(LoanApplication.id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Loan application not found"
        )

    db.delete(application)
    db.commit()

    return {
        "message": "Loan application deleted successfully"
    }

@router.put("/{application_id}/status", response_model=LoanApplicationResponse)
def update_application_status(
    application_id: int,
    status_update: StatusUpdate,
    db: Session = Depends(get_db),
):
    application = (
        db.query(LoanApplication)
        .filter(LoanApplication.id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Loan application not found"
        )

    allowed_statuses = [
        "Pending",
        "Under Review",
        "Verified",
        "Approved",
        "Rejected",
        "Disbursed",
    ]

    if status_update.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Status must be one of: {', '.join(allowed_statuses)}"
        )

    application.status = status_update.status

    db.commit()
    db.refresh(application)

    return application