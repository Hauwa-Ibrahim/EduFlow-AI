import re


def extract_student_information(text: str) -> dict:
    """
    Extract important information from
    an admission letter.

    Returns a dictionary of extracted values.
    """

    result = {
        "student_name": None,
        "institution": None,
        "programme": None,
        "registration_number": None,
        "admission_date": None,
    }

    # -------------------------------
    # Student Name
    # -------------------------------
    name = re.search(
        r"DEAR\s+MS\.?\s*([A-Z\s]+)",
        text,
        re.IGNORECASE,
    )

    if name:
        result["student_name"] = name.group(1).strip()

    # -------------------------------
    # Institution (Improved)
    # -------------------------------
    institution = re.search(
        r"Admissions Board of\s+([A-Za-z\s]+?University)",
        text,
        re.IGNORECASE,
    )

    if institution:
        result["institution"] = institution.group(1).strip()

    # -------------------------------
    # Programme
    # -------------------------------
    programme = re.search(
        r"ADMISSION TO A\s+(.*?)\s+Programme",
        text,
        re.IGNORECASE,
    )

    if programme:
        result["programme"] = programme.group(1).strip()

    # -------------------------------
    # Registration Number
    # -------------------------------
    registration = re.search(
        r"registration number is\s+([A-Za-z0-9\-]+)",
        text,
        re.IGNORECASE,
    )

    if registration:
        result["registration_number"] = registration.group(1)

    # -------------------------------
    # Admission Date
    # -------------------------------
    date = re.search(
        r"(\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+\s+\d{4})",
        text,
        re.IGNORECASE,
    )

    if date:
        result["admission_date"] = date.group(1)

    return result