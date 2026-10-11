from types import SimpleNamespace

from app.agents.search_agent import SearchAgent
from app.agents.analysis_agent import AnalysisAgent
from app.agents.summarizer_agent import SummarizerAgent
from app.agents.critic_agent import CriticAgent
from app.agents.writer_agent import WriterAgent
from app.workflow.graph import build_research_workflow


def test_complete_research_workflow(monkeypatch):
    """Test the complete five-agent workflow without external APIs."""

    papers = ["paper_1", "paper_2"]

    def fake_search(self, query, top_k=5):
        assert query == "large language models"
        return SimpleNamespace(
            papers=papers,
            total_found=len(papers),
        )

    def fake_analyze(self, paper):
        return f"analysis_of_{paper}"

    def fake_summarize(self, analysis):
        return f"summary_of_{analysis}"

    def fake_review(self, analysis):
        return f"review_of_{analysis}"

    def fake_write_report(self, query, analyses, reviews):
        assert query == "large language models"
        assert analyses == [
            "analysis_of_paper_1",
            "analysis_of_paper_2",
        ]
        assert reviews == [
            "review_of_analysis_of_paper_1",
            "review_of_analysis_of_paper_2",
        ]
        return "final_research_report"

    monkeypatch.setattr(SearchAgent, "research_search", fake_search)
    monkeypatch.setattr(AnalysisAgent, "analyze", fake_analyze)
    monkeypatch.setattr(SummarizerAgent, "summarize", fake_summarize)
    monkeypatch.setattr(CriticAgent, "review", fake_review)
    monkeypatch.setattr(WriterAgent, "write_report", fake_write_report)

    workflow = build_research_workflow()

    result = workflow.invoke({
        "query": "large language models",
        "top_k": 2,
    })

    assert result["papers"] == papers
    assert result["total_found"] == 2

    assert result["analyses"] == [
        "analysis_of_paper_1",
        "analysis_of_paper_2",
    ]

    assert result["summaries"] == [
        "summary_of_analysis_of_paper_1",
        "summary_of_analysis_of_paper_2",
    ]

    assert result["reviews"] == [
        "review_of_analysis_of_paper_1",
        "review_of_analysis_of_paper_2",
    ]

    assert result["report"] == "final_research_report"
