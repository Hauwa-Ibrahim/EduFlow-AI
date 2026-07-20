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


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

# Create uploads folder automatically
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
    Upload a PDF document,
    save it,
    extract its text,
    and store its metadata.
    """

    # Verify application exists
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

    # Accept only PDF files
    if (
        file.content_type != "application/pdf"
        or not file.filename.lower().endswith(".pdf")
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed.",
        )

    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}.pdf"
    file_path = UPLOAD_DIR / unique_filename

    try:
        # Save uploaded file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text
        extracted_text = extract_text_from_pdf(str(file_path))

        # Save metadata
        new_document = Document(
            application_id=application_id,
            document_type=document_type,
            file_name=file.filename,
            file_path=str(file_path),
        )

        db.add(new_document)
        db.commit()
        db.refresh(new_document)

        return {
            "message": "Document uploaded successfully",
            "document": {
                "id": new_document.id,
                "application_id": new_document.application_id,
                "document_type": new_document.document_type,
                "file_name": new_document.file_name,
                "file_path": new_document.file_path,
                "verification_status": new_document.verification_status,
            },
            "extracted_text": extracted_text,
        }

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document upload failed: {str(e)}",
        )