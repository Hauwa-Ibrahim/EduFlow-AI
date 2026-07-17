from pydantic import BaseModel


class DocumentCreate(BaseModel):
    application_id: int
    document_type: str
    file_name: str
    file_path: str


class DocumentResponse(DocumentCreate):
    id: int
    verification_status: str

    model_config = {
        "from_attributes": True
    }