from difflib import SequenceMatcher
import re


def normalize(text: str) -> str:
    """
    Normalize text before comparison.
    """

    if not text:
        return ""

    text = text.lower()

    # Expand common abbreviations
    replacements = {
        "bsc": "bachelor of science",
        "b.sc": "bachelor of science",
        "msc": "master of science",
        "m.sc": "master of science",
        "phd": "doctor of philosophy",
        "ph.d": "doctor of philosophy",
        "ai": "artificial intelligence",
    }

    for old, new in replacements.items():
        text = re.sub(rf"\b{re.escape(old)}\b", new, text)

    # Remove anything inside brackets
    text = re.sub(r"\(.*?\)", " ", text)

    # Remove degree words that don't affect programme meaning
    remove_words = [
        "bachelor",
        "master",
        "doctor",
        "science",
        "degree",
        "programme",
        "program",
        "of",
    ]

    for word in remove_words:
        text = re.sub(rf"\b{word}\b", " ", text)

    # Remove punctuation
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Collapse spaces
    text = " ".join(text.split())

    return text


def similarity(a: str, b: str) -> float:
    """
    Standard similarity.
    """

    a = normalize(a)
    b = normalize(b)

    if not a or not b:
        return 0.0

    return SequenceMatcher(None, a, b).ratio()


def compare_names(expected: str, actual: str) -> float:
    """
    Compare names while allowing middle names.
    """

    expected_words = set(normalize(expected).split())
    actual_words = set(normalize(actual).split())

    if not expected_words or not actual_words:
        return 0.0

    common = expected_words.intersection(actual_words)

    return len(common) / len(expected_words)


def compare_programmes(expected: str, actual: str) -> float:
    """
    Compare academic programmes.
    """

    expected = normalize(expected)
    actual = normalize(actual)

    if expected in actual:
        return 1.0

    if actual in expected:
        return 1.0

    return SequenceMatcher(None, expected, actual).ratio()


def compare_institutions(expected: str, actual: str) -> float:
    """
    Compare institutions.
    """

    return similarity(expected, actual)


def verify_application(student, extracted_data):
    """
    Verify extracted admission letter
    against the student's application.
    """

    matched = []
    mismatched = []
    field_scores = {}

    full_name = f"{student.first_name} {student.last_name}"

    comparisons = [
        (
            "student_name",
            full_name,
            extracted_data.get("student_name"),
            compare_names,
            0.70,
        ),
        (
            "institution",
            student.institution,
            extracted_data.get("institution"),
            compare_institutions,
            0.80,
        ),
        (
            "programme",
            student.programme,
            extracted_data.get("programme"),
            compare_programmes,
            0.70,
        ),
    ]

    for field, expected, actual, comparator, threshold in comparisons:

        score = comparator(expected, actual)
        field_scores[field] = round(score * 100)

        print("=" * 50)
        print(field.upper())
        print("Expected :", expected)
        print("Actual   :", actual)
        print("Score    :", round(score, 2))

        if score >= threshold:
            matched.append(field)
        else:
            mismatched.append(field)

    total_fields = len(comparisons)
    matched_count = len(matched)

    confidence = round(
        sum(field_scores.values()) / total_fields
    )

    if matched_count == total_fields:
        status = "Verified"

    elif matched_count >= 2:
        status = "Review"

    else:
        status = "Rejected"

    return {
        "verification_status": status,
        "confidence_score": confidence,
        "matched_fields": matched,
        "mismatched_fields": mismatched,
        "field_scores": field_scores,
        "remarks": (
            f"{matched_count} of {total_fields} fields matched."
        ),
    }