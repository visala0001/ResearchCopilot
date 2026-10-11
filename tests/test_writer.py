
from unittest.mock import Mock

import pytest

from app.agents.writer_agent import WriterAgent
from app.models.analysis import PaperAnalysis
from app.models.critic import CriticReview
from app.models.report import ResearchReport


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
        overall_assessment="The reported result has supporting evidence in the supplied analysis.",
        claim_reviews=[],
        strengths=["The analysis includes relevant evidence."],
        issues_found=[],
        missing_evidence=[],
        recommendations=["Verify important claims against the original paper."],
        confidence="medium",
        evidence_limitations=["Only the supplied analysis was reviewed."],
    )


def create_test_report():
    return ResearchReport(
        title="Transformer Models for Text Classification",
        abstract="This report reviews a supplied study of Transformer models.",
        introduction="Text classification is an important NLP task.",
        research_objectives=["Review the supplied study."],
        literature_review="The supplied paper investigates Transformer-based classification.",
        methodology_comparison="Only one paper was supplied, so cross-paper comparison is limited.",
        key_findings=["The paper reports an accuracy of 92.4%."],
        critical_analysis="The reported result should be interpreted within the paper's limitations.",
        research_gaps=["Additional datasets could be evaluated."],
        future_directions=["Evaluate the method on additional datasets."],
        conclusion="The supplied analysis describes a Transformer-based classification approach.",
        references=["A Study of Transformer Models (bibliographic details not supplied)."],
        limitations_of_review=["Only one paper analysis was supplied."],
    )


def test_writer_returns_structured_report(monkeypatch):
    agent = WriterAgent()
    fake_report = create_test_report()
    generate_mock = Mock(return_value=fake_report)

    monkeypatch.setattr(
        agent.llm,
        "generate_structured",
        generate_mock,
    )

    result = agent.write_report(
        query="How are Transformer models used in text classification?",
        analyses=[create_test_analysis()],
        reviews=[create_test_review()],
    )

    assert isinstance(result, ResearchReport)
    assert result.title == "Transformer Models for Text Classification"
    assert len(result.key_findings) == 1

    generate_mock.assert_called_once()
    assert generate_mock.call_args.kwargs["response_schema"] is ResearchReport

    prompt = generate_mock.call_args.kwargs["prompt"]
    assert "Transformer models" in prompt
    assert "92.4%" in prompt
    assert "Never invent papers" in prompt
    assert "CRITIC REVIEWS" in prompt


def test_writer_rejects_empty_query():
    agent = WriterAgent()

    with pytest.raises(ValueError, match="Research query cannot be empty"):
        agent.write_report(
            query="  ",
            analyses=[create_test_analysis()],
            reviews=[create_test_review()],
        )


def test_writer_rejects_missing_analyses():
    agent = WriterAgent()

    with pytest.raises(ValueError, match="At least one paper analysis"):
        agent.write_report(
            query="Test research question",
            analyses=[],
            reviews=[],
        )


def test_writer_rejects_mismatched_reviews():
    agent = WriterAgent()

    with pytest.raises(ValueError, match="corresponding critic review"):
        agent.write_report(
            query="Test research question",
            analyses=[create_test_analysis()],
            reviews=[],
        )


def test_writer_rejects_empty_llm_response(monkeypatch):
    agent = WriterAgent()

    monkeypatch.setattr(
        agent.llm,
        "generate_structured",
        Mock(return_value=None),
    )

    with pytest.raises(ValueError, match="returned no report"):
        agent.write_report(
            query="Test research question",
            analyses=[create_test_analysis()],
            reviews=[create_test_review()],
        )
