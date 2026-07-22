from pydantic import BaseModel


class OfficerReview(BaseModel):

    decision: str

    comment: str


class OfficerReviewResponse(BaseModel):

    application_id: int

    status: str

    officer_decision: str

    officer_comment: str

    reviewed_by: str

    reviewed_at: str

    class Config:
        from_attributes = True