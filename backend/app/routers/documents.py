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

from app.services.pdf_service import extract_text_from_pdf
from app.services.ai_extractor import extract_student_information
from app.services.verification_service import verify_application
from app.services.eligibility import evaluate_eligibility
from app.services.decision_engine import generate_ai_decision
from app.services.application_service import update_application_from_ai


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

    Workflow:
    1. Save uploaded PDF
    2. Extract text (OCR)
    3. Extract structured student information
    4. Verify against student application
    5. Evaluate eligibility
    6. Generate AI decision
    7. Save document
    8. Update loan application
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

        extracted_text = extract_text_from_pdf(
            str(file_path)
        )

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
        # Save document record
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
        # Update application using AI results
        # ---------------------------------------------------------

        update_application_from_ai(
            application,
            eligibility_result,
            ai_decision,
        )

        # ---------------------------------------------------------
        # Commit transaction
        # ---------------------------------------------------------

        db.commit()

        db.refresh(new_document)
        db.refresh(application)

        # ---------------------------------------------------------
        # Success Response
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

            # Full OCR text (useful during development)
            "extracted_text": extracted_text,
        }

    except Exception as e:

        db.rollback()

        # Remove uploaded file if an error occurred
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document upload failed: {str(e)}",
        )