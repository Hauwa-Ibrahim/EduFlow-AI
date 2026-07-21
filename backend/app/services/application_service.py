def update_application_from_ai(
    application,
    eligibility_result,
    ai_decision,
):
    """
    Update a loan application with AI evaluation results.
    """

    application.eligibility_score = eligibility_result[
        "eligibility_score"
    ]

    application.recommendation = eligibility_result[
        "recommendation"
    ]

    application.risk_level = eligibility_result[
        "risk_level"
    ]

    application.ai_confidence = eligibility_result[
        "confidence_score"
    ]

    application.verification_status = eligibility_result[
        "verification_status"
    ]

    application.status = ai_decision[
        "application_status"
    ]

    return application