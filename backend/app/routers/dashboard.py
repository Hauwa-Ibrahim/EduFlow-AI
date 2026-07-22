from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.application import LoanApplication
from app.models.user import User
from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/")
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Executive dashboard summary.
    """

    total = db.query(LoanApplication).count()

    pending = (
        db.query(LoanApplication)
        .filter(LoanApplication.status == "Pending")
        .count()
    )

    review = (
        db.query(LoanApplication)
        .filter(LoanApplication.status == "Under Review")
        .count()
    )

    approved = (
        db.query(LoanApplication)
        .filter(LoanApplication.status == "Approved")
        .count()
    )

    rejected = (
        db.query(LoanApplication)
        .filter(LoanApplication.status == "Rejected")
        .count()
    )

    disbursed = (
        db.query(LoanApplication)
        .filter(LoanApplication.status == "Disbursed")
        .count()
    )

    average_score = (
        db.query(
            func.avg(
                LoanApplication.eligibility_score
            )
        ).scalar()
        or 0
    )

    average_ai_confidence = (
        db.query(
            func.avg(
                LoanApplication.ai_confidence
            )
        ).scalar()
        or 0
    )

    high_risk = (
        db.query(LoanApplication)
        .filter(
            LoanApplication.risk_level == "High"
        )
        .count()
    )

    medium_risk = (
        db.query(LoanApplication)
        .filter(
            LoanApplication.risk_level == "Medium"
        )
        .count()
    )

    low_risk = (
        db.query(LoanApplication)
        .filter(
            LoanApplication.risk_level == "Low"
        )
        .count()
    )

    return {
        "applications": {
            "total": total,
            "pending": pending,
            "under_review": review,
            "approved": approved,
            "rejected": rejected,
            "disbursed": disbursed,
        },
        "risk_distribution": {
            "low": low_risk,
            "medium": medium_risk,
            "high": high_risk,
        },
        "ai_metrics": {
            "average_eligibility_score": round(
                average_score,
                2,
            ),
            "average_ai_confidence": round(
                average_ai_confidence,
                2,
            ),
        },
    }