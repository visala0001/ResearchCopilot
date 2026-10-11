from pydantic import BaseModel, Field
from typing import Optional


class Paper(BaseModel):
    paper_id: str
    title: str
    abstract: Optional[str] = None
    authors: list[str] = Field(default_factory=list)
    year: Optional[int] = None
    venue: Optional[str] = None
    url: Optional[str] = None
    citation_count: Optional[int] = None

class SearchResult(BaseModel):
    query: str
    papers: list[Paper] = Field(default_factory=list)
    total_found: int = 0

class SearchQueries(BaseModel):
    original_query: str
    queries: list[str] = Field(default_factory=list)