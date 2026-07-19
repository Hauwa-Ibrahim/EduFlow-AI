from pathlib import Path
import shutil

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
)
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.document import Document
from app.models.application import LoanApplication

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

# Create uploads directory automatically
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/")
def create_document(
    application_id: int = Form(...),
    document_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload a student document and save its information.
    """

    # Check loan application exists
    application = (
        db.query(LoanApplication)
        .filter(LoanApplication.id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Loan application not found",
        )

    # Save uploaded file
    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save document record
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
    }