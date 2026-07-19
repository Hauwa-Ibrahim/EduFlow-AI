import fitz


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract all text from a PDF document.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        A single string containing all extracted text.
    """

    document = fitz.open(pdf_path)

    extracted_text = ""

    for page in document:
        extracted_text += page.get_text()

    document.close()

    return extracted_text.strip()