
from app.models.analysis import PaperAnalysis
from app.models.critic import CriticReview
from app.models.report import ResearchReport
from app.services.llm_service import GeminiService


class WriterAgent:
    """Generates an evidence-aware research report from reviewed papers."""

    def __init__(self):
        self.llm = GeminiService()

    def write_report(
        self,
        query: str,
        analyses: list[PaperAnalysis],
        reviews: list[CriticReview],
    ) -> ResearchReport:
        """Generate a structured report from analyses and critic reviews."""

        if not query or not query.strip():
            raise ValueError("Research query cannot be empty.")

        if not analyses:
            raise ValueError("At least one paper analysis is required.")

        if len(analyses) != len(reviews):
            raise ValueError(
                "Each paper analysis must have a corresponding critic review."
            )

        analyses_text = "\n\n".join(
            f"""
Paper {index}:
Title: {analysis.title}
Research problem: {analysis.research_problem}
Research objective: {analysis.research_objective}
Methodology: {analysis.methodology}
Models and algorithms: {analysis.models_and_algorithms}
Datasets: {analysis.datasets}
Experimental setup: {analysis.experimental_setup}
Evaluation metrics: {analysis.evaluation_metrics}
Quantitative results: {analysis.quantitative_results}
Key findings: {analysis.key_findings}
Strengths: {analysis.strengths}
Limitations: {analysis.limitations}
Future work: {analysis.future_work}
Reported facts: {analysis.reported_facts}
Cautious inferences: {analysis.cautious_inferences}
Evidence: {analysis.evidence}
Source type: {analysis.source_type}
Unavailable information: {analysis.unavailable_information}
""".strip()
            for index, analysis in enumerate(analyses, start=1)
        )

        reviews_text = "\n\n".join(
            f"""
Review for paper {index}:
Title: {review.title}
Overall assessment: {review.overall_assessment}
Claim reviews: {review.claim_reviews}
Strengths: {review.strengths}
Issues found: {review.issues_found}
Missing evidence: {review.missing_evidence}
Recommendations: {review.recommendations}
Confidence: {review.confidence}
Evidence limitations: {review.evidence_limitations}
""".strip()
            for index, review in enumerate(reviews, start=1)
        )

        prompt = f"""
You are an academic research writer.

Write a clear, coherent, well-organized research report that answers
the user's research question using the supplied paper analyses and
their corresponding Critic reviews.

RESEARCH QUESTION:
{query.strip()}

PAPER ANALYSES:
{analyses_text}

CRITIC REVIEWS:
{reviews_text}

WRITING RULES:
1. Base the report only on the supplied analyses and reviews.
2. Never invent papers, authors, publication years, URLs, citations,
   datasets, measurements, or experimental results.
3. Attribute findings to papers by their available titles.
4. Distinguish reported findings from interpretations and hypotheses.
5. Do not present an unverifiable claim as an established fact.
6. Respect contradictions and evidence limitations identified by the Critic.
7. Compare methodologies only where the supplied information permits it.
8. Identify research gaps as potential gaps suggested by the reviewed material,
   not as proof that no prior research exists.
9. If bibliographic details are missing, state that limitation rather than
   fabricating a reference.
10. Use precise academic language and avoid repetitive filler.
11. Make the conclusion directly address the research question.
12. Return a complete structured report matching the supplied schema.

The report should contain an abstract, introduction, research objectives,
literature review, methodology comparison, key findings, critical analysis,
research gaps, future directions, conclusion, references, and limitations
of the review.
"""

        result = self.llm.generate_structured(
            prompt=prompt,
            response_schema=ResearchReport,
        )

        if result is None:
            raise ValueError("The Writing Agent returned no report.")

        return result
