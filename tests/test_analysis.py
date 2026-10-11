
from unittest.mock import Mock

import pytest

from app.agents.analysis_agent import AnalysisAgent
from app.models.analysis import PaperAnalysis
from app.models.paper import Paper


def create_test_paper(
    url=None,
    abstract="This paper studies Transformer models for text classification.",
):
    return Paper(
        paper_id="test-paper-1",
        title="A Study of Transformer Models",
        abstract=abstract,
        authors=["Test Author"],
        year=2025,
        url=url,
    )


def create_test_analysis():
    return PaperAnalysis(
        title="A Study of Transformer Models",
        research_problem="Text classification performance.",
        methodology="Transformer-based classification.",
        key_findings=["The paper reports its findings."],
        strengths=["The method is clearly described."],
        limitations=["Further validation may be needed."],
        future_work=["Evaluate additional datasets."],
        datasets=["Dataset A"],
        evaluation_metrics=["Accuracy"],
        quantitative_results=["Accuracy: 92.4%"],
        reported_facts=["The paper reports an accuracy of 92.4%."],
        evidence=["[Page 2] The reported accuracy is 92.4%."],
    )


def test_analysis_uses_full_pdf_text(monkeypatch):
    agent = AnalysisAgent()
    document = Mock()

    monkeypatch.setattr(
        agent.pdf_loader,
        "load_pdf",
        lambda url: document,
    )
    monkeypatch.setattr(
        agent.text_extractor,
        "extract_text",
        lambda doc: "[Page 1] Full research paper content.",
    )

    close_mock = Mock()
    document.close = close_mock

    fake_analysis = create_test_analysis()
    generate_mock = Mock(return_value=fake_analysis)
    monkeypatch.setattr(
        agent.llm,
        "generate_structured",
        generate_mock,
    )

    result = agent.analyze(
        create_test_paper(
            url="https://example.com/paper.pdf"
        )
    )

    assert isinstance(result, PaperAnalysis)
    assert result.source_type == "full_text"
    assert result.title == "A Study of Transformer Models"
    assert "Accuracy: 92.4%" in result.quantitative_results

    prompt = generate_mock.call_args.kwargs["prompt"]
    assert "Full research paper content" in prompt
    assert "full_text" in prompt

    document.close.assert_called_once()


def test_analysis_falls_back_to_abstract_when_pdf_fails(monkeypatch):
    agent = AnalysisAgent()

    monkeypatch.setattr(
        agent.pdf_loader,
        "load_pdf",
        Mock(side_effect=RuntimeError("Download failed")),
    )

    fake_analysis = create_test_analysis()
    monkeypatch.setattr(
        agent.llm,
        "generate_structured",
        Mock(return_value=fake_analysis),
    )

    result = agent.analyze(
        create_test_paper(
            url="https://example.com/paper.pdf"
        )
    )

    assert result.source_type == "abstract_only"
    assert any(
        "abstract only" in item.lower()
        for item in result.unavailable_information
    )


def test_analysis_uses_abstract_when_no_url(monkeypatch):
    agent = AnalysisAgent()
    fake_analysis = create_test_analysis()

    generate_mock = Mock(return_value=fake_analysis)
    monkeypatch.setattr(
        agent.llm,
        "generate_structured",
        generate_mock,
    )

    result = agent.analyze(create_test_paper(url=None))

    assert result.source_type == "abstract_only"

    prompt = generate_mock.call_args.kwargs["prompt"]
    assert "Transformer models for text classification" in prompt


def test_analysis_rejects_missing_title():
    agent = AnalysisAgent()

    paper = create_test_paper()
    paper.title = ""

    with pytest.raises(ValueError, match="title"):
        agent.analyze(paper)


def test_analysis_rejects_missing_pdf_and_abstract(monkeypatch):
    agent = AnalysisAgent()

    monkeypatch.setattr(
        agent.pdf_loader,
        "load_pdf",
        Mock(side_effect=RuntimeError("Download failed")),
    )

    paper = create_test_paper(
        url="https://example.com/paper.pdf",
        abstract=None,
    )

    with pytest.raises(ValueError, match="no readable PDF text or abstract"):
        agent.analyze(paper)


def test_analysis_rejects_invalid_llm_response(monkeypatch):
    agent = AnalysisAgent()

    monkeypatch.setattr(
        agent.llm,
        "generate_structured",
        Mock(return_value={"title": "Invalid response"}),
    )

    with pytest.raises(RuntimeError, match="valid PaperAnalysis"):
        agent.analyze(create_test_paper(url=None))
