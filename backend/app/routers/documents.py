from pathlib import Path
import shutil
import uuid

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
    status,
)
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.application import LoanApplication
from app.models.document import Document
from app.models.user import User

from app.auth.dependencies import get_current_user
from app.models.notification import Notification

from app.services.pdf_service import extract_text_from_pdf
from app.services.ai_extractor import extract_student_information
from app.services.verification_service import verify_application
from app.services.eligibility import evaluate_eligibility
from app.services.decision_engine import generate_ai_decision
from app.services.application_service import update_application_from_ai
from app.services.audit_service import create_audit_log


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

# ---------------------------------------------------------
# Upload directory
# ---------------------------------------------------------

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_document(
    application_id: int = Form(...),
    document_type: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Upload a PDF document.

    Workflow

    1. Save uploaded PDF
    2. OCR Extraction
    3. AI Information Extraction
    4. Verification
    5. Eligibility Evaluation
    6. AI Decision
    7. Save Document
    8. Update Application
    9. Create Audit Log
    """

    # ---------------------------------------------------------
    # Fetch Loan Application
    # ---------------------------------------------------------

    application = (
        db.query(LoanApplication)
        .filter(LoanApplication.id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan application not found",
        )

    # ---------------------------------------------------------
    # Validate uploaded file
    # ---------------------------------------------------------

    if (
        file.content_type != "application/pdf"
        or not file.filename.lower().endswith(".pdf")
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed.",
        )

    unique_filename = f"{uuid.uuid4()}.pdf"
    file_path = UPLOAD_DIR / unique_filename

    try:
        # ---------------------------------------------------------
        # Save uploaded PDF
        # ---------------------------------------------------------

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ---------------------------------------------------------
        # OCR Extraction
        # ---------------------------------------------------------

        extracted_text = extract_text_from_pdf(str(file_path))

        # ---------------------------------------------------------
        # AI Information Extraction
        # ---------------------------------------------------------

        structured_data = extract_student_information(
            extracted_text
        )

        student = application.student

        # ---------------------------------------------------------
        # AI Verification
        # ---------------------------------------------------------

        verification_result = verify_application(
            student,
            structured_data,
        )

        # ---------------------------------------------------------
        # AI Eligibility
        # ---------------------------------------------------------

        eligibility_result = evaluate_eligibility(
            student=student,
            application=application,
            verification_result=verification_result,
        )

        # ---------------------------------------------------------
        # AI Decision
        # ---------------------------------------------------------

        ai_decision = generate_ai_decision(
            eligibility_result
        )

        # ---------------------------------------------------------
        # Save Document
        # ---------------------------------------------------------

        new_document = Document(
            application_id=application_id,
            document_type=document_type,
            file_name=file.filename,
            file_path=str(file_path),
            verification_status=verification_result[
                "verification_status"
            ],
            confidence_score=verification_result[
                "confidence_score"
            ],
            matched_fields=",".join(
                verification_result["matched_fields"]
            ),
            mismatched_fields=",".join(
                verification_result["mismatched_fields"]
            ),
        )

        db.add(new_document)

        # ---------------------------------------------------------
        # Update Application
        # ---------------------------------------------------------

        update_application_from_ai(
            application,
            eligibility_result,
            ai_decision,
        )

        # ---------------------------------------------------------
        # Audit Log
        # ---------------------------------------------------------

        create_audit_log(
            db=db,
            application_id=application.id,
            action="Document Uploaded",
            performed_by=current_user.email,
            details=f"{document_type} uploaded and processed by AI",
        )

        # ---------------------------------------------------------
        # Create Notification
        # ---------------------------------------------------------

        if application.status == "Approved":
            title = "Loan Application Approved"
            message = (
                "Congratulations! Your loan application has been approved."
            )

        elif application.status == "Rejected":
            title = "Loan Application Rejected"
            message = (
                "Your loan application was rejected after AI document verification."
            )

        elif application.status == "Under Review":
            title = "Application Under Review"
            message = (
                "Your application is currently under review by our loan team."
            )

        elif application.status == "Verified":
            title = "Documents Verified"
            message = (
                "Your admission documents have been successfully verified."
            )

        elif application.status == "Disbursed":
            title = "Loan Disbursed"
            message = (
                "Congratulations! Your student loan has been successfully disbursed."
            )

        else:
            title = "Loan Application Update"
            message = (
                f"Your application status is now {application.status}."
            )

        notification = Notification(
            student_id=application.student_id,
            title=title,
            message=message,
            notification_type="Application",
        )

        db.add(notification)

        # ---------------------------------------------------------
        # Commit
        # ---------------------------------------------------------

        db.commit()

        db.refresh(new_document)
        db.refresh(application)

        # ---------------------------------------------------------
        # Response
        # ---------------------------------------------------------

        return {
            "message": "Document uploaded successfully",
            "application": {
                "id": application.id,
                "status": application.status,
                "eligibility_score": application.eligibility_score,
                "recommendation": application.recommendation,
                "risk_level": application.risk_level,
                "ai_confidence": application.ai_confidence,
                "verification_status": application.verification_status,
            },
            "document": {
                "id": new_document.id,
                "application_id": new_document.application_id,
                "document_type": new_document.document_type,
                "file_name": new_document.file_name,
                "file_path": new_document.file_path,
                "verification_status": new_document.verification_status,
                "confidence_score": new_document.confidence_score,
                "matched_fields": new_document.matched_fields,
                "mismatched_fields": new_document.mismatched_fields,
            },
            "structured_data": structured_data,
            "verification_result": verification_result,
            "eligibility_result": eligibility_result,
            "ai_decision": ai_decision,
            "extracted_text": extracted_text,
        }

    except Exception as e:

        db.rollback()

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document upload failed: {str(e)}",
        )