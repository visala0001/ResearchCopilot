
from typing import Literal

from pydantic import BaseModel, Field


ClaimVerdict = Literal[
    "supported",
    "contradicted",
    "partially_supported",
    "unverifiable",
]


class ClaimReview(BaseModel):
    """Evidence-based review of an individual research claim."""

    claim: str = Field(
        description="The exact research claim being reviewed"
    )

    verdict: ClaimVerdict = Field(
        description="How the available evidence relates to the claim"
    )

    evidence: list[str] = Field(
        default_factory=list,
        description="Evidence from the provided research material"
    )

    explanation: str = Field(
        description="Reasoning that explains the verdict"
    )

    suggested_correction: str | None = Field(
        default=None,
        description="A more accurate version of the claim, if needed"
    )


class CriticReview(BaseModel):
    """Structured quality and evidence review of a research analysis."""

    title: str = Field(
        description="Title of the research paper being reviewed"
    )

    overall_assessment: str = Field(
        description="Overall assessment of the analysis and its evidence"
    )

    claim_reviews: list[ClaimReview] = Field(
        default_factory=list,
        description="Evidence-based verdicts for individual claims"
    )

    strengths: list[str] = Field(
        default_factory=list,
        description="Well-supported aspects of the analysis"
    )

    issues_found: list[str] = Field(
        default_factory=list,
        description="Unsupported statements, inconsistencies, or reasoning issues"
    )

    missing_evidence: list[str] = Field(
        default_factory=list,
        description="Claims or conclusions that need additional evidence"
    )

    recommendations: list[str] = Field(
        default_factory=list,
        description="Specific recommendations to improve accuracy and clarity"
    )

    confidence: Literal["low", "medium", "high"] = Field(
        description="Confidence in the review, based on evidence quality"
    )

    evidence_limitations: list[str] = Field(
        default_factory=list,
        description="Limits of the available source material"
    )
