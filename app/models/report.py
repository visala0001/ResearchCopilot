
from pydantic import BaseModel, Field


class ResearchReport(BaseModel):
    """Structured research report generated from reviewed research."""

    title: str = Field(
        description="Title of the research report"
    )

    abstract: str = Field(
        description="Concise overview of the report"
    )

    introduction: str = Field(
        description="Background, context, and motivation"
    )

    research_objectives: list[str] = Field(
        default_factory=list,
        description="Research questions or objectives addressed"
    )

    literature_review: str = Field(
        description="Synthesis of the available research papers"
    )

    methodology_comparison: str = Field(
        description="Comparison of methods used across the reviewed papers"
    )

    key_findings: list[str] = Field(
        default_factory=list,
        description="Main findings, attributed to the relevant papers"
    )

    critical_analysis: str = Field(
        description="Strengths, limitations, disagreements, and evidence gaps"
    )

    research_gaps: list[str] = Field(
        default_factory=list,
        description="Research gaps suggested by the available evidence"
    )

    future_directions: list[str] = Field(
        default_factory=list,
        description="Potential directions for future research"
    )

    conclusion: str = Field(
        description="Evidence-based conclusion addressing the research question"
    )

    references: list[str] = Field(
        default_factory=list,
        description="References for the reviewed papers using available bibliographic details"
    )

    limitations_of_review: list[str] = Field(
        default_factory=list,
        description="Limitations caused by incomplete sources or available evidence"
    )
