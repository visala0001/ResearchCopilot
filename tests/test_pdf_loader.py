
from unittest.mock import Mock, patch

import pymupdf as fitz
import pytest
import requests

from app.tools.pdf_loader import PDFLoader


def create_test_pdf() -> bytes:
    """Create a tiny valid PDF in memory for testing."""
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "ResearchCopilot PDF test.")
    pdf_bytes = document.tobytes()
    document.close()
    return pdf_bytes


def mock_pdf_response(pdf_bytes: bytes):
    """Create a mock streaming HTTP response."""
    response = Mock()
    response.headers = {
        "Content-Type": "application/pdf",
        "Content-Length": str(len(pdf_bytes)),
    }
    response.iter_content.return_value = [pdf_bytes]
    response.raise_for_status.return_value = None
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=False)
    return response


def test_load_pdf_successfully():
    pdf_bytes = create_test_pdf()
    response = mock_pdf_response(pdf_bytes)

    with patch("app.tools.pdf_loader.requests.get", return_value=response):
        document = PDFLoader().load_pdf("https://example.com/paper.pdf")

    try:
        assert document.page_count == 1
        assert "ResearchCopilot PDF test" in document[0].get_text()
    finally:
        document.close()


def test_load_pdf_rejects_empty_url():
    with pytest.raises(ValueError, match="URL cannot be empty"):
        PDFLoader().load_pdf("")


def test_load_pdf_rejects_non_http_url():
    with pytest.raises(ValueError, match="http:// or https://"):
        PDFLoader().load_pdf("paper.pdf")


def test_load_pdf_rejects_non_pdf_response():
    response = mock_pdf_response(b"This is not a PDF.")

    with patch("app.tools.pdf_loader.requests.get", return_value=response):
        with pytest.raises(ValueError, match="valid PDF"):
            PDFLoader().load_pdf("https://example.com/paper")


def test_load_pdf_rejects_oversized_content():
    pdf_bytes = create_test_pdf()
    response = mock_pdf_response(pdf_bytes)

    with patch("app.tools.pdf_loader.requests.get", return_value=response):
        loader = PDFLoader(max_file_size=10)

        with pytest.raises(ValueError, match="maximum allowed file size"):
            loader.load_pdf("https://example.com/paper.pdf")


def test_load_pdf_handles_network_timeout():
    with patch(
        "app.tools.pdf_loader.requests.get",
        side_effect=requests.exceptions.Timeout("Request timed out"),
    ):
        with pytest.raises(RuntimeError, match="Failed to download PDF"):
            PDFLoader().load_pdf("https://example.com/paper.pdf")
