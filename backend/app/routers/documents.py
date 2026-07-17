from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.document import Document
from app.models.application import LoanApplication
from app.schemas.document import DocumentCreate, DocumentResponse

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post(
    "/",
    response_model=DocumentResponse
)
def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db)
):
    # Check that the loan application exists
    application = (
        db.query(LoanApplication)
        .filter(LoanApplication.id == document.application_id)
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Loan application not found"
        )

    # Create the document
    new_document = Document(
        application_id=document.application_id,
        document_type=document.document_type,
        file_name=document.file_name,
        file_path=document.file_path,
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return new_document