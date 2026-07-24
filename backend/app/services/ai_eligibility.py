from app.models.application import LoanApplication


def assess_application(application: LoanApplication):
    """
    Rule-based AI Eligibility Assessment.
    Recalculates eligibility every time an application is viewed.
    """

    score = 0
    reasons = []

    # Institution check
    if application.student.institution:
        score += 20
        reasons.append("Eligible institution provided.")

    # Programme check
    if application.student.programme:
        score += 15
        reasons.append("Programme information available.")

    # Documents uploaded
    if application.documents:
        score += 25
        reasons.append("Required document(s) uploaded.")

    # Documents verified
    if application.documents and all(
        doc.verification_status == "Verified"
        for doc in application.documents
    ):
        score += 25
        reasons.append("All uploaded documents verified.")

    # Loan amount check
    if application.amount_requested <= 500000:
        score += 15
        reasons.append("Requested loan amount is within policy limit.")

    # Recommendation
    if score >= 80:
        recommendation = "Approved"
        risk = "Low"
    elif score >= 60:
        recommendation = "Review"
        risk = "Medium"
    else:
        recommendation = "Rejected"
        risk = "High"

    return {
        "eligibility_score": score,
        "recommendation": recommendation,
        "risk_level": risk,
        "ai_confidence": min(score, 100),
        "reason": " ".join(reasons),
    }