from app.models.student import Student
from app.models.application import LoanApplication


def evaluate_eligibility(
    student: Student,
    application: LoanApplication,
    verification_result: dict,
):
    """
    Enterprise Loan Eligibility Engine

    Maximum Score = 100

    Categories:
    - Student Information
    - Loan Application
    - Document Verification
    - AI Confidence
    """

    score = 0
    reasons = []
    score_breakdown = {}

    verification_status = verification_result.get(
        "verification_status",
        "Rejected",
    )

    confidence_score = verification_result.get(
        "confidence_score",
        0,
    )

    # -----------------------------
    # Student Information (40 Marks)
    # -----------------------------

    student_score = 0

    if student:
        student_score += 10
        reasons.append("Student record found.")

    if student.institution:
        student_score += 15
        reasons.append("Institution provided.")

    if student.programme:
        student_score += 15
        reasons.append("Programme provided.")

    score += student_score
    score_breakdown["student"] = student_score

    # -----------------------------
    # Loan Application (20 Marks)
    # -----------------------------

    application_score = 0

    if application.status == "Pending":
        application_score += 10
        reasons.append("Application is active.")

    if application.amount_requested > 0:
        application_score += 5
        reasons.append("Loan amount requested.")

    if application.academic_session:
        application_score += 5
        reasons.append("Academic session provided.")

    score += application_score
    score_breakdown["application"] = application_score

    # -----------------------------
    # Document Verification (30 Marks)
    # -----------------------------

    verification_score = 0

    if verification_status == "Verified":
        verification_score = 30
        reasons.append("Admission document verified.")

    elif verification_status == "Review":
        verification_score = 15
        reasons.append("Admission document requires manual review.")

    else:
        verification_score = 0
        reasons.append("Admission document verification failed.")

    score += verification_score
    score_breakdown["verification"] = verification_score

    # -----------------------------
    # AI Confidence (10 Marks)
    # -----------------------------

    ai_score = 0

    if confidence_score >= 95:
        ai_score = 10
        reasons.append("Excellent AI confidence.")

    elif confidence_score >= 85:
        ai_score = 8
        reasons.append("Very high AI confidence.")

    elif confidence_score >= 70:
        ai_score = 5
        reasons.append("Moderate AI confidence.")

    else:
        ai_score = 0
        reasons.append("Low AI confidence.")

    score += ai_score
    score_breakdown["ai_confidence"] = ai_score

    # -----------------------------
    # Cap Score
    # -----------------------------

    score = min(score, 100)

    # -----------------------------
    # Recommendation
    # -----------------------------

    if score >= 90:
        recommendation = "Approve"
        risk_level = "Low"

    elif score >= 70:
        recommendation = "Manual Review"
        risk_level = "Medium"

    elif score >= 50:
        recommendation = "High Risk Review"
        risk_level = "High"

    else:
        recommendation = "Reject"
        risk_level = "Critical"

    return {
        "eligibility_score": score,
        "recommendation": recommendation,
        "risk_level": risk_level,
        "verification_status": verification_status,
        "confidence_score": confidence_score,
        "score_breakdown": score_breakdown,
        "reasons": reasons,
    }