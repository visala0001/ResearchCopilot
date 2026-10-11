from app.models.analysis import PaperAnalysis
from app.models.summary import PaperSummary
from app.agents.summarizer_agent import SummarizerAgent


def create_test_analysis() -> PaperAnalysis:

    return PaperAnalysis(
        title="Attention Is All You Need",

        research_problem=(
            "The paper addresses limitations of recurrent sequence models."
        ),

        methodology=(
            "The authors introduce the Transformer architecture based entirely "
            "on attention mechanisms."
        ),

        key_findings=[
            "The Transformer achieved strong translation performance.",
            "The architecture supports greater parallelization."
        ],

        strengths=[
            "Highly parallelizable.",
            "Effective long-range dependency modeling."
        ],

        limitations=[
            "Self-attention can be expensive for long sequences."
        ],

        future_work=[
            "Develop efficient attention mechanisms."
        ]
    )


def test_summarizer_returns_paper_summary():

    analysis = create_test_analysis()

    agent = SummarizerAgent()

    result = agent.summarize(analysis)

    # Verify that Gemini returned the expected Pydantic model
    assert isinstance(result, PaperSummary)

    assert result.title
    assert result.executive_summary
    assert len(result.key_contributions) > 0
    assert len(result.key_findings) > 0
    assert len(result.limitations) > 0
    assert len(result.future_work) > 0

    # Display the generated summary
    print("\n")
    print("=" * 70)
    print("GENERATED PAPER SUMMARY")
    print("=" * 70)

    print("\nTITLE:")
    print(result.title)

    print("\nEXECUTIVE SUMMARY:")
    print(result.executive_summary)

    print("\nRESEARCH PROBLEM:")
    print(result.research_problem)

    print("\nMETHODOLOGY:")
    print(result.methodology)

    print("\nKEY CONTRIBUTIONS:")
    for item in result.key_contributions:
        print(f"- {item}")

    print("\nKEY FINDINGS:")
    for item in result.key_findings:
        print(f"- {item}")

    print("\nSTRENGTHS:")
    for item in result.strengths:
        print(f"- {item}")

    print("\nLIMITATIONS:")
    for item in result.limitations:
        print(f"- {item}")

    print("\nFUTURE WORK:")
    for item in result.future_work:
        print(f"- {item}")

    print("\n")
    print("=" * 70)
    print("SUMMARIZER AGENT TEST PASSED")
    print("=" * 70)