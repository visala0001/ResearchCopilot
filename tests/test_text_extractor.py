
import pymupdf as fitz
import pytest

from app.tools.text_extractor import TextExtractor


def create_pdf(text: str = "ResearchCopilot extraction test.") -> fitz.Document:
    """Create a one-page PDF in memory."""
    document = fitz.open()
    page = document.new_page()

    if text:
        page.insert_text((72, 72), text)

    return document


def test_extract_text_successfully():
    document = create_pdf(
        "ResearchCopilot extraction test."
    )

    try:
        text = TextExtractor().extract_text(document)

        assert "ResearchCopilot extraction test." in text
        assert "[Page 1]" in text
    finally:
        document.close()


def test_extract_text_from_multiple_pages():
    document = fitz.open()

    first_page = document.new_page()
    first_page.insert_text((72, 72), "First page content.")

    second_page = document.new_page()
    second_page.insert_text((72, 72), "Second page content.")

    try:
        text = TextExtractor().extract_text(document)

        assert "[Page 1]" in text
        assert "First page content." in text
        assert "[Page 2]" in text
        assert "Second page content." in text
    finally:
        document.close()


def test_extract_text_rejects_empty_document():
    document = fitz.open()

    try:
        with pytest.raises(ValueError, match="no pages"):
            TextExtractor().extract_text(document)
    finally:
        document.close()


def test_extract_text_rejects_image_only_or_blank_pdf():
    document = create_pdf(text="")

    try:
        with pytest.raises(ValueError, match="No readable text"):
            TextExtractor().extract_text(document)
    finally:
        document.close()


def test_extract_text_respects_max_pages():
    document = fitz.open()

    for page_number in range(3):
        page = document.new_page()
        page.insert_text(
            (72, 72),
            f"Content from page {page_number + 1}."
        )

    try:
        text = TextExtractor(max_pages=2).extract_text(document)

        assert "Content from page 1." in text
        assert "Content from page 2." in text
        assert "Content from page 3." not in text
    finally:
        document.close()


def test_max_pages_must_be_positive():
    with pytest.raises(ValueError, match="max_pages"):
        TextExtractor(max_pages=0)
