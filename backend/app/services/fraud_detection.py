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
    Analyze an application for potential fraud indicators.
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

    # -----------------------------------
    # Low AI confidence
    # -----------------------------------

    if confidence < 60:
        fraud_score += 25
        flags.append("Low AI confidence")

    # -----------------------------------
    # Verification failed
    # -----------------------------------

    if verification_result["verification_status"] == "Rejected":
        fraud_score += 30
        flags.append("Document verification failed")

    # -----------------------------------
    # Institution mismatch
    # -----------------------------------

    if institution != application.student.institution:
        fraud_score += 20
        flags.append("Institution mismatch")

    # -----------------------------------
    # Programme mismatch
    # -----------------------------------

    if programme != application.student.programme:
        fraud_score += 15
        flags.append("Programme mismatch")

    # -----------------------------------
    # Duplicate registration number
    # -----------------------------------

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
                "Registration number already exists"
            )

    # -----------------------------------
    # Risk Level
    # -----------------------------------

    if fraud_score >= 60:
        risk = "High"
        recommendation = "Escalate Investigation"

    elif fraud_score >= 30:
        risk = "Medium"
        recommendation = "Manual Review"

    else:
        risk = "Low"
        recommendation = "Proceed"

    return {

        "fraud_score": fraud_score,

        "risk_level": risk,

        "recommendation": recommendation,

        "flags": flags,
    }