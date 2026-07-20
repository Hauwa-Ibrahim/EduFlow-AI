from difflib import SequenceMatcher


def similarity(a: str, b: str) -> float:
    """
    Calculate similarity between two strings.
    Returns a value between 0 and 1.
    """

    if not a or not b:
        return 0.0

    return SequenceMatcher(
        None,
        a.lower().strip(),
        b.lower().strip(),
    ).ratio()


def verify_application(student, extracted_data):
    """
    Compare the student's application with the
    extracted admission letter information.
    """

    matched = []
    mismatched = []

    # -------------------------
    # Student Name
    # -------------------------
    full_name = f"{student.first_name} {student.last_name}"

    if similarity(
        full_name,
        extracted_data.get("student_name"),
    ) >= 0.70:
        matched.append("student_name")
    else:
        mismatched.append("student_name")

    # -------------------------
    # Institution
    # -------------------------
    if similarity(
        student.institution,
        extracted_data.get("institution"),
    ) >= 0.75:
        matched.append("institution")
    else:
        mismatched.append("institution")

    # -------------------------
    # Programme
    # -------------------------
    if similarity(
        student.programme,
        extracted_data.get("programme"),
    ) >= 0.70:
        matched.append("programme")
    else:
        mismatched.append("programme")

    # -------------------------
    # Confidence Score
    # -------------------------
    confidence_score = round((len(matched) / 3) * 100)

    # -------------------------
    # Verification Decision
    # -------------------------
    if confidence_score >= 90:
        verification_status = "Verified"
    elif confidence_score >= 60:
        verification_status = "Review"
    else:
        verification_status = "Rejected"

    return {
        "verification_status": verification_status,
        "confidence_score": confidence_score,
        "matched_fields": matched,
        "mismatched_fields": mismatched,
    }