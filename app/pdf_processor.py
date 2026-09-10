import os
from pypdf import PdfReader


def extract_pages_from_pdf(pdf_path):
    """
    Extract PDF text page-by-page along with source filename
    and page number.

    Returns:
        [
            {
                "source": "document.pdf",
                "page": 1,
                "text": "..."
            }
        ]
    """

    pages = []

    if not pdf_path or not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    try:
        reader = PdfReader(pdf_path)

        for page_number, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()

            if page_text and page_text.strip():
                pages.append(
                    {
                        "source": os.path.basename(pdf_path),
                        "page": page_number,
                        "text": page_text.strip(),
                    }
                )

    except Exception as e:
        raise RuntimeError(
            f"Error processing PDF '{pdf_path}': {str(e)}"
        )

    return pages


def extract_text_from_pdf(pdf_path):
    """
    Backward-compatible function.

    Returns all PDF text as one string.
    """

    pages = extract_pages_from_pdf(pdf_path)

    text_parts = []

    for item in pages:
        text_parts.append(item["text"])

    return "\n\n".join(text_parts).strip()