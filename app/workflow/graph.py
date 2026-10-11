from langgraph.graph import StateGraph, START, END

from app.agents.search_agent import SearchAgent
from app.agents.analysis_agent import AnalysisAgent
from app.agents.summarizer_agent import SummarizerAgent
from app.agents.critic_agent import CriticAgent
from app.agents.writer_agent import WriterAgent

from app.workflow.state import ResearchState


def search_node(state: ResearchState) -> ResearchState:
    """Search for relevant research papers."""

    agent = SearchAgent()

    result = agent.research_search(
        query=state["query"],
        top_k=5,
    )

    state["papers"] = result.papers
    state["total_found"] = result.total_found

    return state


def analysis_node(state: ResearchState) -> ResearchState:
    """Analyze each paper returned by the Search Agent."""

    agent = AnalysisAgent()
    papers = state.get("papers", [])

    state["analyses"] = [
        agent.analyze(paper)
        for paper in papers
    ]

    return state


def summarizer_node(state: ResearchState) -> ResearchState:
    """Summarize each analysis produced by the Analysis Agent."""

    agent = SummarizerAgent()
    analyses = state.get("analyses", [])

    state["summaries"] = [
        agent.summarize(analysis)
        for analysis in analyses
    ]

    return state


def critic_node(state: ResearchState) -> ResearchState:
    """Review each analysis for evidence support and reliability."""

    agent = CriticAgent()
    analyses = state.get("analyses", [])

    state["reviews"] = [
        agent.review(analysis)
        for analysis in analyses
    ]

    return state


def writer_node(state: ResearchState) -> ResearchState:
    """Generate the final research report from analyses and reviews."""

    agent = WriterAgent()

    state["report"] = agent.write_report(
        query=state["query"],
        analyses=state.get("analyses", []),
        reviews=state.get("reviews", []),
    )

    return state


def build_search_workflow():
    """Build the original search-only workflow."""

    workflow = StateGraph(ResearchState)

    workflow.add_node("search", search_node)
    workflow.add_edge(START, "search")
    workflow.add_edge("search", END)

    return workflow.compile()


def build_research_workflow():
    """Build the complete multi-agent research workflow."""

    workflow = StateGraph(ResearchState)

    workflow.add_node("search", search_node)
    workflow.add_node("analysis", analysis_node)
    workflow.add_node("summarizer", summarizer_node)
    workflow.add_node("critic", critic_node)
    workflow.add_node("writer", writer_node)

    workflow.add_edge(START, "search")
    workflow.add_edge("search", "analysis")
    workflow.add_edge("analysis", "summarizer")
    workflow.add_edge("summarizer", "critic")
    workflow.add_edge("critic", "writer")
    workflow.add_edge("writer", END)

    return workflow.compile()
