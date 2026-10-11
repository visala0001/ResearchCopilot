from app.agents.search_agent import SearchAgent
from app.models.paper import Paper, SearchResult
from app.workflow.graph import search_node, build_search_workflow


def test_search_node(monkeypatch):

    paper1 = Paper(
        paper_id="1",
        title="Large Language Models in Healthcare",
        abstract="Research on LLM applications in healthcare.",
        authors=["Alice"],
        year=2025
    )

    paper2 = Paper(
        paper_id="2",
        title="Clinical Applications of LLMs",
        abstract="Study of language models in clinical settings.",
        authors=["Bob"],
        year=2024
    )

    fake_result = SearchResult(
        query="large language models healthcare",
        papers=[paper1, paper2],
        total_found=2
    )

    def fake_research_search(self, query, top_k):
        return fake_result

    monkeypatch.setattr(
        SearchAgent,
        "research_search",
        fake_research_search
    )

    state = {
        "query": "large language models healthcare"
    }

    result = search_node(state)

    assert result["query"] == "large language models healthcare"

    assert result["total_found"] == 2

    assert len(result["papers"]) == 2

    assert result["papers"][0].paper_id == "1"
    assert result["papers"][1].paper_id == "2"

def test_search_workflow(monkeypatch):

    paper = Paper(
        paper_id="1",
        title="Large Language Models",
        abstract="Research on large language models.",
        authors=["Alice"],
        year=2025
    )

    fake_result = SearchResult(
        query="large language models",
        papers=[paper],
        total_found=1
    )

    def fake_research_search(self, query, top_k):
        return fake_result

    monkeypatch.setattr(
        SearchAgent,
        "research_search",
        fake_research_search
    )

    workflow = build_search_workflow()

    initial_state = {
        "query": "large language models"
    }

    result = workflow.invoke(initial_state)

    assert result["query"] == "large language models"

    assert result["total_found"] == 1

    assert len(result["papers"]) == 1

    assert result["papers"][0].paper_id == "1"