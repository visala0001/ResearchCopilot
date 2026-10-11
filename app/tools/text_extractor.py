
import pymupdf as fitz


class TextExtractor:
    """Extract and validate readable text from a PDF document."""

    def __init__(self, max_pages: int = 100):
        if max_pages <= 0:
            raise ValueError("max_pages must be greater than 0.")

        self.max_pages = max_pages

    def extract_text(self, document: fitz.Document) -> str:
        """
        Extract text from a PDF document.

        Raises:
            ValueError: If the document has no pages or readable text.
        """
        if document.page_count == 0:
            raise ValueError("PDF contains no pages.")

        page_count = min(document.page_count, self.max_pages)
        extracted_pages = []

        for page_number in range(page_count):
            page = document.load_page(page_number)
            page_text = page.get_text("text")

            if page_text and page_text.strip():
                extracted_pages.append(
                    f"[Page {page_number + 1}]\n{page_text.strip()}"
                )

        text = "\n\n".join(extracted_pages).strip()

        if not text:
            raise ValueError(
                "No readable text found in the PDF. "
                "It may be scanned or image-only."
            )

        return text
