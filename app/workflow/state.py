from typing import TypedDict

from app.models.paper import Paper
from app.models.analysis import PaperAnalysis
from app.models.summary import PaperSummary
from app.models.critic import CriticReview
from app.models.report import ResearchReport


class ResearchState(TypedDict, total=False):
    """Shared state passed between ResearchCopilot workflow nodes."""

    query: str
    search_queries: list[str]
    top_k: int

    papers: list[Paper]
    total_found: int

    analyses: list[PaperAnalysis]
    summaries: list[PaperSummary]

    reviews: list[CriticReview]
    report: ResearchReport
