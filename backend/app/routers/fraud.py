from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.application import LoanApplication
from app.models.document import Document
from app.models.user import User

from app.auth.dependencies import get_current_user

from app.services.fraud_detection import analyze_fraud
from app.services.ai_extractor import extract_student_information
from app.services.pdf_service import extract_text_from_pdf


router = APIRouter(
    prefix="/fraud",
    tags=["Fraud Detection"],
)


@router.post("/check/{application_id}")
def check_fraud(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Run AI fraud detection for a loan application.
    """

    application = (
        db.query(LoanApplication)
        .filter(LoanApplication.id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Loan application not found.",
        )

    # Get the latest uploaded document
    document = (
        db.query(Document)
        .filter(Document.application_id == application_id)
        .order_by(Document.id.desc())
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="No document found for this application.",
        )

    # OCR
    extracted_text = extract_text_from_pdf(
        document.file_path
    )

    # AI Extraction
    structured_data = extract_student_information(
        extracted_text
    )

    # Build verification result from stored document
    verification_result = {
        "verification_status": document.verification_status,
        "confidence_score": document.confidence_score,
    }

    # Fraud Analysis
    fraud_result = analyze_fraud(
        db=db,
        application=application,
        structured_data=structured_data,
        verification_result=verification_result,
    )

    return {
        "application_id": application.id,
        "student_id": application.student_id,
        "fraud_analysis": fraud_result,
    }