from pydantic import BaseModel


class LoanApplicationCreate(BaseModel):
    student_id: int
    loan_type: str
    academic_session: str
    amount_requested: int


class LoanApplicationResponse(LoanApplicationCreate):
    id: int
    status: str

    class Config:
        from_attributes = True