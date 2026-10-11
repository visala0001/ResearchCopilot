
from app.models.paper import Paper
from app.models.analysis import PaperAnalysis
from app.tools.pdf_loader import PDFLoader
from app.tools.text_extractor import TextExtractor
from app.services.llm_service import GeminiService
from app.prompts.analysis_prompt import build_analysis_prompt


class AnalysisAgent:
    """Analyze a research paper using its PDF or abstract."""

    def __init__(self):
        self.pdf_loader = PDFLoader()
        self.text_extractor = TextExtractor()
        self.llm = GeminiService()

    def analyze(self, paper: Paper) -> PaperAnalysis:
        """Analyze one paper and return a structured analysis."""

        if not paper.title or not paper.title.strip():
            raise ValueError("Paper title cannot be empty.")

        source_text = ""
        source_type = "abstract_only"

        # First, try to retrieve and extract the full paper.
        if paper.url:
            document = None

            try:
                document = self.pdf_loader.load_pdf(paper.url)
                extracted_text = self.text_extractor.extract_text(document)

                if extracted_text.strip():
                    source_text = extracted_text
                    source_type = "full_text"

            except (ValueError, RuntimeError):
                # A URL may point to a webpage, a missing file,
                # or an unreadable PDF. Try the abstract instead.
                pass

            finally:
                if document is not None:
                    document.close()

        # Fall back to the abstract when the PDF is unavailable.
        if not source_text.strip():
            abstract = (paper.abstract or "").strip()

            if not abstract:
                raise ValueError(
                    "Cannot analyze paper: no readable PDF text "
                    "or abstract is available."
                )

            source_text = abstract
            source_type = "abstract_only"

        prompt = build_analysis_prompt(
            title=paper.title,
            source_type=source_type,
            source_text=source_text,
        )

        analysis = self.llm.generate_structured(
            prompt=prompt,
            response_schema=PaperAnalysis,
        )

        if not isinstance(analysis, PaperAnalysis):
            raise RuntimeError(
                "Gemini did not return a valid PaperAnalysis result."
            )

        # Keep the original source identity explicit.
        analysis.title = paper.title
        analysis.source_type = source_type

        if source_type == "abstract_only":
            note = (
                "Full paper text was not available; "
                "analysis is based on the abstract only."
            )

            if note not in analysis.unavailable_information:
                analysis.unavailable_information.append(note)

        return analysis
