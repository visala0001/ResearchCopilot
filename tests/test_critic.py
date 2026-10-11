
from unittest.mock import Mock

import pytest

from app.agents.critic_agent import CriticAgent
from app.models.analysis import PaperAnalysis
from app.models.critic import ClaimReview, CriticReview


def create_test_analysis():
    return PaperAnalysis(
        title="A Study of Transformer Models",
        research_problem="Evaluate Transformer models for text classification.",
        methodology="Transformer-based classification.",
        key_findings=["The paper reports its findings."],
        strengths=["The method is clearly described."],
        limitations=["Further validation may be needed."],
        future_work=["Evaluate additional datasets."],
        quantitative_results=["Accuracy: 92.4%"],
        reported_facts=["The paper reports an accuracy of 92.4%."],
        evidence=["[Page 2] The reported accuracy is 92.4%."],
    )


def create_test_review():
    return CriticReview(
        title="A Study of Transformer Models",
        overall_assessment="The analysis contains a reported result with supporting evidence.",
        claim_reviews=[
            ClaimReview(
                claim="The paper reports an accuracy of 92.4%.",
                verdict="supported",
                evidence=["[Page 2] The reported accuracy is 92.4%."],
                explanation="The provided evidence matches the reported claim.",
            )
        ],
        strengths=["The result is linked to available evidence."],
        issues_found=[],
        missing_evidence=[],
        recommendations=["Check the original paper before making independent claims."],
        confidence="medium",
        evidence_limitations=["Only the supplied analysis was reviewed."],
    )


def test_critic_returns_structured_review(monkeypatch):
    agent = CriticAgent()
    fake_review = create_test_review()

    generate_mock = Mock(return_value=fake_review)
    monkeypatch.setattr(
        agent.llm,
        "generate_structured",
        generate_mock,
    )

    result = agent.review(create_test_analysis())

    assert isinstance(result, CriticReview)
    assert result.title == "A Study of Transformer Models"
    assert result.claim_reviews[0].verdict == "supported"
    assert result.confidence == "medium"

    generate_mock.assert_called_once()
    assert generate_mock.call_args.kwargs["response_schema"] is CriticReview

    prompt = generate_mock.call_args.kwargs["prompt"]
    assert "92.4%" in prompt
    assert "Do not invent facts" in prompt
    assert "unverifiable" in prompt.lower()


def test_critic_rejects_empty_llm_response(monkeypatch):
    agent = CriticAgent()

    monkeypatch.setattr(
        agent.llm,
        "generate_structured",
        Mock(return_value=None),
    )

    with pytest.raises(ValueError, match="returned no review"):
        agent.review(create_test_analysis())


def test_critic_review_model_accepts_unverifiable_claim():
    review = ClaimReview(
        claim="The method is better than every competing method.",
        verdict="unverifiable",
        evidence=[],
        explanation="The provided analysis contains no comparative evidence.",
    )

    assert review.verdict == "unverifiable"
    assert review.suggested_correction is None
