from pydantic import BaseModel, Field
from typing import List


class PaperSummary(BaseModel):
    title: str = Field(
        description="Title of the research paper"
    )

    executive_summary: str = Field(
        description="A concise overall summary of the research paper"
    )

    research_problem: str = Field(
        description="The problem the paper attempts to solve"
    )

    methodology: str = Field(
        description="A concise explanation of the methodology used"
    )

    key_contributions: List[str] = Field(
        description="The major contributions of the research"
    )

    key_findings: List[str] = Field(
        description="The most important findings of the research"
    )

    strengths: List[str] = Field(
        description="Important strengths of the research"
    )

    limitations: List[str] = Field(
        description="Important limitations of the research"
    )

    future_work: List[str] = Field(
        description="Potential future research directions"
    )