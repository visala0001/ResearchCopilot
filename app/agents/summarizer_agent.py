from app.models.analysis import PaperAnalysis
from app.models.summary import PaperSummary
from app.prompts.summarizer_prompt import build_summarizer_prompt
from app.services.llm_service import GeminiService


class SummarizerAgent:

    def __init__(self):
        self.llm = GeminiService()

    def summarize(self, analysis: PaperAnalysis) -> PaperSummary:

        prompt = build_summarizer_prompt(
            analysis.model_dump()
        )

        summary = self.llm.generate_structured(
            prompt=prompt,
            response_schema=PaperSummary,
        )

        return summary