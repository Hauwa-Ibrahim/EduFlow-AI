from pydantic import BaseModel


class DocumentCreate(BaseModel):
    application_id: int
    document_type: str
    file_name: str
    file_path: str


class DocumentResponse(DocumentCreate):
    id: int
    verification_status: str
    confidence_score: int | None = None

    model_config = {
        "from_attributes": True
    }


# ==========================================================
# Document Summary
# ==========================================================

class DocumentSummaryResponse(BaseModel):
    id: int
    document_type: str
    verification_status: str
    confidence_score: int | None = None

    model_config = {
        "from_attributes": True
    }