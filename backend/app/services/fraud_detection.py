from sqlalchemy.orm import Session

from app.models.application import LoanApplication
from app.models.document import Document


def analyze_fraud(
    db: Session,
    application: LoanApplication,
    structured_data: dict,
    verification_result: dict,
):
    """
    AI Fraud Detection Engine

    Analyses a loan application for possible fraud indicators
    and returns a fraud score, risk level and recommendation.
    """

    fraud_score = 0
    flags = []

    registration_number = structured_data.get(
        "registration_number"
    )

    institution = structured_data.get(
        "institution"
    )

    programme = structured_data.get(
        "programme"
    )

    confidence = verification_result.get(
        "confidence_score",
        0,
    )

    verification_status = verification_result.get(
        "verification_status",
        "Rejected",
    )

    student = application.student

    # ---------------------------------------------------------
    # AI Confidence
    # ---------------------------------------------------------

    if confidence < 60:
        fraud_score += 25
        flags.append(
            "Low AI confidence."
        )

    # ---------------------------------------------------------
    # Document Verification
    # ---------------------------------------------------------

    if verification_status == "Rejected":
        fraud_score += 30
        flags.append(
            "Admission document verification failed."
        )

    elif verification_status == "Review":
        fraud_score += 15
        flags.append(
            "Document requires manual review."
        )

    # ---------------------------------------------------------
    # Institution Mismatch
    # ---------------------------------------------------------

    if (
        institution
        and student
        and institution.strip().lower()
        != student.institution.strip().lower()
    ):
        fraud_score += 20
        flags.append(
            "Institution does not match student record."
        )

    # ---------------------------------------------------------
    # Programme Mismatch
    # ---------------------------------------------------------

    if (
        programme
        and student
        and programme.strip().lower()
        != student.programme.strip().lower()
    ):
        fraud_score += 15
        flags.append(
            "Programme does not match student record."
        )

    # ---------------------------------------------------------
    # Duplicate Registration Number
    # ---------------------------------------------------------

    if registration_number:

        duplicate = (
            db.query(Document)
            .filter(
                Document.matched_fields.contains(
                    registration_number
                )
            )
            .first()
        )

        if duplicate:

            fraud_score += 25

            flags.append(
                "Registration number already exists."
            )

    # ---------------------------------------------------------
    # Determine Risk Level
    # ---------------------------------------------------------

    if fraud_score >= 60:

        risk_level = "High"
        recommendation = "Escalate Investigation"
        status = "Fraud Suspected"

    elif fraud_score >= 30:

        risk_level = "Medium"
        recommendation = "Manual Review"
        status = "Needs Investigation"

    else:

        risk_level = "Low"
        recommendation = "Proceed"
        status = "Clean"

    # ---------------------------------------------------------
    # No Issues Found
    # ---------------------------------------------------------

    if not flags:

        flags.append(
            "No fraud indicators detected."
        )

    # ---------------------------------------------------------
    # Response
    # ---------------------------------------------------------

    return {

        "fraud_score": fraud_score,

        "risk_level": risk_level,

        "status": status,

        "recommendation": recommendation,

        "flags": flags,
    }