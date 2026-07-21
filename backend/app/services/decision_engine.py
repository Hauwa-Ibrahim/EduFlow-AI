def generate_ai_decision(eligibility_result: dict):
    """
    Generate the final AI decision for a loan application.
    """

    score = eligibility_result["eligibility_score"]
    recommendation = eligibility_result["recommendation"]
    risk = eligibility_result["risk_level"]

    if recommendation == "Approve":
        application_status = "Under Review"

        reason = (
            "Application meets eligibility requirements "
            "and is ready for officer approval."
        )

    elif recommendation == "Manual Review":
        application_status = "Under Review"

        reason = (
            "Application requires additional review "
            "before approval."
        )

    else:
        application_status = "Rejected"

        reason = (
            "Application failed eligibility assessment."
        )

    return {
        "decision": recommendation,
        "application_status": application_status,
        "risk_level": risk,
        "reason": reason,
    }