from pydantic import BaseModel

from app.schemas.student import StudentResponse
from app.schemas.document import DocumentSummaryResponse


# ==========================================================
# Create Application
# ==========================================================

class LoanApplicationCreate(BaseModel):
    student_id: int
    loan_type: str
    academic_session: str
    amount_requested: int


# ==========================================================
# Application List Response
# Used by GET /applications
# ==========================================================

class LoanApplicationResponse(LoanApplicationCreate):
    id: int
    status: str

    # AI Decision Fields
    eligibility_score: int | None = None
    recommendation: str | None = None
    risk_level: str | None = None
    ai_confidence: int | None = None
    verification_status: str | None = None

    class Config:
        from_attributes = True


# ==========================================================
# Officer Review Summary
# ==========================================================

class OfficerReviewSummary(BaseModel):
    decision: str | None = None
    comment: str | None = None
    reviewed_by: str | None = None
    reviewed_at: str | None = None


# ==========================================================
# Application Details Response
# Used by GET /applications/{id}
# ==========================================================

class ApplicationDetailsResponse(BaseModel):
    id: int
    student_id: int
    loan_type: str
    academic_session: str
    amount_requested: int
    status: str

    # AI Decision Fields
    eligibility_score: int | None = None
    recommendation: str | None = None
    risk_level: str | None = None
    ai_confidence: int | None = None
    verification_status: str | None = None

    # Related Student
    student: StudentResponse | None = None

    # Related Documents
    documents: list[DocumentSummaryResponse] = []

    # Officer Review
    officer_review: OfficerReviewSummary | None = None

    class Config:
        from_attributes = True