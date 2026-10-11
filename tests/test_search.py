import pytest

from app.agents.search_agent import SearchAgent
from app.models.paper import Paper, SearchQueries, SearchResult
from app.tools.semantic_scholar import SemanticScholarTool


@pytest.mark.integration
def test_search_returns_papers():

    tool = SemanticScholarTool()

    papers = tool.search_papers(
        query="large language models",
        limit=3
    )

    assert isinstance(papers, list)
    assert len(papers) <= 3

    for paper in papers:
        assert isinstance(paper, Paper)
        assert paper.paper_id
        assert paper.title

def test_empty_query():

    tool = SemanticScholarTool()

    with pytest.raises(ValueError):
        tool.search_papers("")


def test_invalid_limit():

    tool = SemanticScholarTool()

    with pytest.raises(ValueError):
        tool.search_papers("machine learning", 0)


@pytest.mark.integration
def test_search_agent_returns_search_result():

    agent = SearchAgent()

    result = agent.search(
        query="large language models",
        top_k=3
    )

    assert isinstance(result, SearchResult)
    assert result.query == "large language models"
    assert isinstance(result.papers, list)
    assert result.total_found == len(result.papers)

    assert len(result.papers) <= 3


def test_search_agent_empty_query():

    agent = SearchAgent()

    with pytest.raises(ValueError):
        agent.search("", top_k=3)


def test_search_agent_invalid_top_k():

    agent = SearchAgent()

    with pytest.raises(ValueError):
        agent.search("machine learning",top_k=0)

def test_search_agent_with_mocked_tool(monkeypatch):

    fake_papers = [
        Paper(
            paper_id="1",
            title="Large Language Models",
            authors=["Alice"],
            year=2025
        ),
        Paper(
            paper_id="2",
            title="Transformers for NLP",
            authors=["Bob"],
            year=2024
        ),
    ]

    def fake_search_papers(query, limit):
        return fake_papers[:limit]

    agent = SearchAgent()

    monkeypatch.setattr(
        agent.search_tool,
        "search_papers",
        fake_search_papers
    )

    result = agent.search(
        query="large language models",
        top_k=2
    )

    assert isinstance(result, SearchResult)
    assert len(result.papers) == 2
    assert result.papers[0].title == "Large Language Models"
    assert result.papers[1].title == "Transformers for NLP"

@pytest.mark.integration
def test_generate_queries():

    agent = SearchAgent()

    result = agent.generate_queries(
        "How are large language models used in healthcare?"
    )

    assert isinstance(result, SearchQueries)

    assert result.original_query == (
        "How are large language models used in healthcare?"
    )

    assert 3 <= len(result.queries) <= 5

    for query in result.queries:
        assert isinstance(query, str)
        assert query.strip()

def test_deduplicate_papers():

    agent = SearchAgent()

    papers = [
        Paper(
            paper_id="1",
            title="Paper One",
            authors=["Alice"]
        ),
        Paper(
            paper_id="2",
            title="Paper Two",
            authors=["Bob"]
        ),
        Paper(
            paper_id="1",
            title="Paper One",
            authors=["Alice"]
        ),
    ]

    unique_papers = agent._deduplicate_papers(papers)

    assert len(unique_papers) == 2
    assert unique_papers[0].paper_id == "1"
    assert unique_papers[1].paper_id == "2"

def test_search_with_queries_and_deduplication(monkeypatch):

    agent = SearchAgent()

    paper1 = Paper(
        paper_id="1",
        title="Paper One",
        authors=["Alice"]
    )

    paper2 = Paper(
        paper_id="2",
        title="Paper Two",
        authors=["Bob"]
    )

    paper3 = Paper(
        paper_id="3",
        title="Paper Three",
        authors=["Charlie"]
    )

    def fake_search_papers(query, limit):

        if query == "query one":
            return [paper1, paper2]

        if query == "query two":
            return [paper2, paper3]

        return []

    monkeypatch.setattr(
        agent.search_tool,
        "search_papers",
        fake_search_papers
    )

    result = agent.search_with_queries(
        queries=["query one", "query two"],
        top_k=5
    )

    assert len(result.papers) == 3
    assert result.total_found == 3

    assert [p.paper_id for p in result.papers] == [
        "1",
        "2",
        "3"
    ]

def test_filter_relevant_papers():

    agent = SearchAgent()

    relevant = Paper(
        paper_id="1",
        title="Large Language Models in Healthcare",
        abstract="Applications of language models in clinical medicine."
    )

    irrelevant = Paper(
        paper_id="2",
        title="Computer Vision for Autonomous Vehicles",
        abstract="Deep learning methods for object detection."
    )

    papers = agent._filter_relevant_papers(
        [relevant, irrelevant],
        "large language models healthcare"
    )

    assert len(papers) == 1
    assert papers[0].paper_id == "1"

def test_rank_papers():

    agent = SearchAgent()

    paper1 = Paper(
        paper_id="1",
        title="Healthcare Applications of Large Language Models",
        abstract="Large language models are increasingly used in healthcare."
    )

    paper2 = Paper(
        paper_id="2",
        title="Machine Learning",
        abstract="Some applications include language models."
    )

    ranked = agent._rank_papers(
        [paper2, paper1],
        "large language models healthcare"
    )

    assert ranked[0].paper_id == "1"
    assert ranked[1].paper_id == "2"

def test_complete_research_search(monkeypatch):

    agent = SearchAgent()

    generated_queries = SearchQueries(
        original_query="large language models healthcare",
        queries=[
            "large language models healthcare",
            "LLM clinical applications",
            "generative AI healthcare"
        ]
    )

    paper1 = Paper(
        paper_id="1",
        title="Large Language Models in Healthcare",
        abstract=(
            "Large language models are being used "
            "for healthcare applications."
        ),
        authors=["Alice"],
        year=2025,
        citation_count=100
    )

    paper2 = Paper(
        paper_id="2",
        title="LLM Clinical Applications",
        abstract=(
            "This paper studies clinical applications "
            "of large language models."
        ),
        authors=["Bob"],
        year=2024,
        citation_count=80
    )

    paper3 = Paper(
        paper_id="3",
        title="Generative AI in Healthcare",
        abstract=(
            "Generative AI has several applications "
            "in modern healthcare."
        ),
        authors=["Charlie"],
        year=2023,
        citation_count=50
    )

    duplicate_paper = Paper(
        paper_id="1",
        title="Large Language Models in Healthcare",
        abstract=(
            "Large language models are being used "
            "for healthcare applications."
        ),
        authors=["Alice"],
        year=2025,
        citation_count=100
    )

    def fake_generate_queries(query):
        return generated_queries

    def fake_search_papers(query, limit):

        if query == "large language models healthcare":
            return [paper1, paper2]

        if query == "LLM clinical applications":
            return [paper2, paper3]

        if query == "generative AI healthcare":
            return [duplicate_paper, paper3]

        return []

    monkeypatch.setattr(
        agent,
        "generate_queries",
        fake_generate_queries
    )

    monkeypatch.setattr(
        agent.search_tool,
        "search_papers",
        fake_search_papers
    )

    result = agent.research_search(
        query="large language models healthcare",
        top_k=2
    )

    assert isinstance(result, SearchResult)

    assert result.query == "large language models healthcare"

    assert result.total_found == 2

    assert len(result.papers) == 2

    paper_ids = [
        paper.paper_id
        for paper in result.papers
    ]

    assert len(set(paper_ids)) == 2

    assert "1" in paper_ids
    assert "2" in paper_ids

def test_research_search_handles_search_error(monkeypatch):

    agent = SearchAgent()

    generated_queries = SearchQueries(
        original_query="machine learning",
        queries=["machine learning"]
    )

    def fake_generate_queries(query):
        return generated_queries

    def fake_search_papers(query, limit):
        raise RuntimeError("Semantic Scholar unavailable")

    monkeypatch.setattr(
        agent,
        "generate_queries",
        fake_generate_queries
    )

    monkeypatch.setattr(
        agent.search_tool,
        "search_papers",
        fake_search_papers
    )

    with pytest.raises(
        RuntimeError,
        match="Semantic Scholar unavailable"
    ):
        agent.research_search(
            query="machine learning",
            top_k=5
        )


def test_research_search_empty_generated_queries(monkeypatch):

    agent = SearchAgent()

    empty_queries = SearchQueries(
        original_query="machine learning",
        queries=[]
    )

    def fake_generate_queries(query):
        return empty_queries

    def fake_search_papers(query, limit):
        return [
            Paper(
                paper_id="paper-1",
                title="Machine Learning Research",
                abstract="Research about machine learning methods.",
                authors=["Test Author"],
                year=2024,
                venue="Test Conference",
                url="https://example.com/paper",
                citation_count=10,
            )
        ]

    monkeypatch.setattr(
        agent,
        "generate_queries",
        fake_generate_queries
    )

    monkeypatch.setattr(
        agent.search_tool,
        "search_papers",
        fake_search_papers
    )

    result = agent.research_search("machine learning", top_k=5)

    assert result.query == "machine learning"
    assert len(result.papers) == 1
    assert result.papers[0].paper_id == "paper-1"
