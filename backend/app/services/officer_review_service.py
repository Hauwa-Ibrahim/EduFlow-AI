from datetime import datetime

from app.models.application import LoanApplication
from app.services.audit_service import create_audit_log
from app.services.notification_service import create_notification

ALLOWED_DECISIONS = [
    "Approved",
    "Rejected",
    "Request Documents",
    "Disbursed",
]


def review_application(
    db,
    application: LoanApplication,
    decision: str,
    comment: str,
    reviewer: str,
):
    """
    Apply an officer's review and create an audit log.
    """

    if decision not in ALLOWED_DECISIONS:
        raise ValueError(
            f"Decision must be one of: {', '.join(ALLOWED_DECISIONS)}"
        )

    application.officer_decision = decision
    application.officer_comment = comment
    application.reviewed_by = reviewer
    application.reviewed_at = datetime.utcnow()

    # Update application status
    application.status = decision


       # ---------------------------------------------------------
    # Audit Log
    # ---------------------------------------------------------

    create_audit_log(
        db=db,
        application_id=application.id,
        action="Officer Review",
        performed_by=reviewer,
        details=f"{decision}: {comment}",
    )

    # ---------------------------------------------------------
    # Student Notification
    # ---------------------------------------------------------

    create_notification(
        db=db,
        student=application.student,
        title="Application Review Completed",
        message=(
            f"Your loan application has been "
            f"{decision.lower()}.\n\n"
            f"Officer Comment:\n{comment}"
        ),
        notification_type="Application",
    )

    return application