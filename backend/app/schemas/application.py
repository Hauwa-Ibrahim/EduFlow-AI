from pydantic import BaseModel


class LoanApplicationCreate(BaseModel):
    student_id: int
    loan_type: str
    academic_session: str
    amount_requested: int


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