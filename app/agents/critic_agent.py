
from app.models.analysis import PaperAnalysis
from app.models.critic import CriticReview
from app.services.llm_service import GeminiService


class CriticAgent:
    """Reviews research analysis for evidence support and reliability."""

    def __init__(self):
        self.llm = GeminiService()

    def review(self, analysis: PaperAnalysis) -> CriticReview:
        """Review an analysis and return a structured evidence-based critique."""

        prompt = f"""
You are an academic research critic and evidence-checking assistant.

Your task is to evaluate the research analysis provided below.

IMPORTANT RULES:
1. Use only the information contained in the provided analysis.
2. Do not invent facts, citations, quotations, results, or evidence.
3. Distinguish supported, contradicted, partially_supported, and unverifiable claims.
4. Do not label a claim false merely because evidence is missing.
5. Treat reported facts as claims to assess, not automatically as verified truth.
6. Identify unsupported conclusions, internal inconsistencies, and overconfident wording.
7. If the source material is incomplete, clearly state the limitation.
8. Suggest corrections only when they are justified by the available evidence.
9. Be objective, precise, and academically responsible.
10. Do not assume that a research paper's reported findings have been independently verified.

Return a structured review matching the supplied response schema.

RESEARCH ANALYSIS:
Title: {analysis.title}

Research problem:
{analysis.research_problem}

Research objective:
{analysis.research_objective or "Not reported"}

Methodology:
{analysis.methodology}

Models and algorithms:
{analysis.models_and_algorithms}

Datasets:
{analysis.datasets}

Experimental setup:
{analysis.experimental_setup}

Evaluation metrics:
{analysis.evaluation_metrics}

Quantitative results:
{analysis.quantitative_results}

Key findings:
{analysis.key_findings}

Strengths:
{analysis.strengths}

Limitations:
{analysis.limitations}

Future work:
{analysis.future_work}

Reported facts:
{analysis.reported_facts}

Cautious inferences:
{analysis.cautious_inferences}

Available evidence:
{analysis.evidence}

Source type:
{analysis.source_type or "Unknown"}

Unavailable information:
{analysis.unavailable_information}

For each reviewed claim, provide its verdict, relevant available evidence,
an explanation, and a suggested correction when appropriate.

If the analysis does not contain enough information to review a claim,
mark it unverifiable rather than guessing.
"""

        result = self.llm.generate_structured(
            prompt=prompt,
            response_schema=CriticReview,
        )

        if result is None:
            raise ValueError("The Critic Agent returned no review.")

        return result
