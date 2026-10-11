
from typing import List

from pydantic import BaseModel, Field


class PaperAnalysis(BaseModel):
    """Structured analysis of a research paper."""

    # Existing fields — preserved for SummarizerAgent compatibility
    title: str = Field(
        description="Title of the research paper"
    )

    research_problem: str = Field(
        description="The main research problem addressed by the paper"
    )

    methodology: str = Field(
        description="The methodology, approach, or experimental method used"
    )

    key_findings: List[str] = Field(
        description="Important findings or results reported by the paper"
    )

    strengths: List[str] = Field(
        description="Main strengths supported by the provided source"
    )

    limitations: List[str] = Field(
        description="Main limitations or weaknesses supported by the source"
    )

    future_work: List[str] = Field(
        description="Future research directions reported or suggested by the paper"
    )

    # Additional research-specific fields
    research_objective: str = Field(
        default="",
        description="The specific objective or goal of the research"
    )

    models_and_algorithms: List[str] = Field(
        default_factory=list,
        description="Models, algorithms, architectures, or techniques used"
    )

    datasets: List[str] = Field(
        default_factory=list,
        description="Datasets used, including names and sizes when reported"
    )

    experimental_setup: str = Field(
        default="",
        description="Experimental setup, baselines, and comparison conditions"
    )

    evaluation_metrics: List[str] = Field(
        default_factory=list,
        description="Evaluation metrics used, including definitions when available"
    )

    quantitative_results: List[str] = Field(
        default_factory=list,
        description=(
            "Numerical results exactly as supported by the source, "
            "including units, percentages, and comparison baselines"
        )
    )

    reported_facts: List[str] = Field(
        default_factory=list,
        description="Facts explicitly stated in the provided source"
    )

    cautious_inferences: List[str] = Field(
        default_factory=list,
        description=(
            "Reasonable interpretations not explicitly stated by the authors; "
            "clearly label each item as an inference"
        )
    )

    evidence: List[str] = Field(
        default_factory=list,
        description=(
            "Supporting evidence with page markers where available; "
            "use short quotations or faithful source-grounded descriptions"
        )
    )

    source_type: str = Field(
        default="unknown",
        description=(
            "Source analyzed: full_text, abstract_only, or unknown"
        )
    )

    unavailable_information: List[str] = Field(
        default_factory=list,
        description=(
            "Important details that cannot be determined from the supplied source"
        )
    )
