
from io import BytesIO

import requests
import pymupdf as fitz


class PDFLoader:
    """Safely download and open research paper PDFs."""

    def __init__(
        self,
        timeout: int = 20,
        max_file_size: int = 20 * 1024 * 1024,
    ):
        self.timeout = timeout
        self.max_file_size = max_file_size

    def load_pdf(self, url: str) -> fitz.Document:
        """
        Download a PDF from a URL and return an open PDF document.

        Raises:
            ValueError: If the URL is empty or the response is not a PDF.
            RuntimeError: If downloading or opening the PDF fails.
        """
        if not url or not url.strip():
            raise ValueError("PDF URL cannot be empty.")

        url = url.strip()

        if not url.lower().startswith(("http://", "https://")):
            raise ValueError("PDF URL must start with http:// or https://.")

        try:
            with requests.get(
                url,
                timeout=self.timeout,
                stream=True,
                headers={"User-Agent": "ResearchCopilot/1.0"},
            ) as response:
                response.raise_for_status()

                content_type = response.headers.get(
                    "Content-Type", ""
                ).lower()

                content_length = response.headers.get("Content-Length")

                if content_length:
                    try:
                        declared_size = int(content_length)
                    except ValueError:
                        declared_size = None

                    if (
                        declared_size is not None
                        and declared_size > self.max_file_size
                    ):
                        raise ValueError(
                            "PDF exceeds the maximum allowed file size."
                        )

                chunks = []
                downloaded_size = 0

                for chunk in response.iter_content(chunk_size=8192):
                    if not chunk:
                        continue

                    downloaded_size += len(chunk)

                    if downloaded_size > self.max_file_size:
                        raise ValueError(
                            "PDF exceeds the maximum allowed file size."
                        )

                    chunks.append(chunk)

                pdf_bytes = b"".join(chunks)

        except ValueError:
            raise
        except requests.exceptions.RequestException as exc:
            raise RuntimeError(
                f"Failed to download PDF: {exc}"
            ) from exc

        if not pdf_bytes:
            raise ValueError("Downloaded file is empty.")

        # Check the PDF file signature rather than trusting only
        # the server's Content-Type header.
        if not pdf_bytes.startswith(b"%PDF-"):
            raise ValueError(
                f"URL did not return a valid PDF file "
                f"(Content-Type: {content_type or 'unknown'})."
            )

        try:
            document = fitz.open(stream=BytesIO(pdf_bytes), filetype="pdf")
        except (fitz.FileDataError, RuntimeError, ValueError) as exc:
            raise ValueError(
                "The downloaded file could not be opened as a PDF."
            ) from exc

        if document.page_count == 0:
            document.close()
            raise ValueError("PDF contains no pages.")

        return document
