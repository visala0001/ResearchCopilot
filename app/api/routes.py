import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.models.paper import Paper
from app.models.analysis import PaperAnalysis
from app.models.summary import PaperSummary
from app.models.critic import CriticReview
from app.models.report import ResearchReport
from app.workflow.graph import build_research_workflow


logger = logging.getLogger(__name__)

router = APIRouter()


class ResearchRequest(BaseModel):
    query: str = Field(
        min_length=1,
        max_length=500,
        description="Research question or topic to investigate",
    )


class ResearchResponse(BaseModel):
    query: str
    total_found: int
    papers: list[Paper]
    analyses: list[PaperAnalysis]
    summaries: list[PaperSummary]
    reviews: list[CriticReview]
    report: ResearchReport | None = None


@router.get("/health")
def health_check():
    """Check whether the API is running."""

    return {
        "status": "ok",
        "service": "ResearchCopilot",
    }


@router.post("/research", response_model=ResearchResponse)
def conduct_research(request: ResearchRequest):
    """Run the complete five-agent research workflow."""

    query = request.query.strip()

    if not query:
        raise HTTPException(
            status_code=422,
            detail="Research query cannot be empty.",
        )

    try:
        workflow = build_research_workflow()

        result = workflow.invoke({
            "query": query,
        })

        return ResearchResponse(
            query=query,
            total_found=result.get("total_found", 0),
            papers=result.get("papers", []),
            analyses=result.get("analyses", []),
            summaries=result.get("summaries", []),
            reviews=result.get("reviews", []),
            report=result.get("report"),
        )

    except HTTPException:
        raise

    except Exception as exc:
        logger.exception("Research workflow failed")

        raise HTTPException(
            status_code=500,
            detail=(
                "Research failed. Check the API terminal "
                "for diagnostic details."
            ),
        ) from exc
