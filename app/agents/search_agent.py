from app.models.paper import SearchResult, SearchQueries
from app.tools.semantic_scholar import SemanticScholarTool
from app.services.llm_service import GeminiService
from app.prompts.search_prompt import SEARCH_QUERY_PROMPT


class SearchAgent:

    def __init__(self):
        self.search_tool = SemanticScholarTool()
        self.llm_service = GeminiService()

    def generate_queries(
        self,
        query: str
    ) -> SearchQueries:

        if not query or not query.strip():
            raise ValueError("Search query cannot be empty.")

        prompt = SEARCH_QUERY_PROMPT.format(
            query=query.strip()
        )

        result = self.llm_service.generate_structured(
            prompt=prompt,
            response_schema=SearchQueries
        )

        return result

    def _deduplicate_papers(self, papers):
        unique_papers = {}
    
        for paper in papers:
            if paper.paper_id not in unique_papers:
                unique_papers[paper.paper_id] = paper
        return list(unique_papers.values())

    def search(
        self,
        query: str,
        top_k: int = 5
    ) -> SearchResult:

        if not query or not query.strip():
            raise ValueError("Search query cannot be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than 0.")

        papers = self.search_tool.search_papers(
            query=query,
            limit=top_k
        )

        return SearchResult(
            query=query,
            papers=papers,
            total_found=len(papers)
        )

    def search_with_queries(
        self,
        queries: list[str],
        top_k: int = 5
    ) -> SearchResult:

        if not queries:
            raise ValueError("At least one search query is required.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than 0.")

        all_papers = []

        for query in queries:

            if not query or not query.strip():
                continue

            papers = self.search_tool.search_papers(
                query=query.strip(),
                limit=top_k
            )

            all_papers.extend(papers)

        unique_papers = self._deduplicate_papers(all_papers)

        return SearchResult(
            query=" | ".join(queries),
            papers=unique_papers[:top_k],
            total_found=len(unique_papers)
        )

    def research_search(
        self,
        query: str,
        top_k: int = 5
    ) -> SearchResult:

        if not query or not query.strip():
            raise ValueError("Search query cannot be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than 0.")

        search_queries = self.generate_queries(query)
        if not search_queries.queries:
            raise ValueError("No search queries generated from the research question.")
        all_papers = []

        for search_query in search_queries.queries:

            papers = self.search_tool.search_papers(
                query=search_query,
                limit=top_k
            )

            all_papers.extend(papers)

        unique_papers = self._deduplicate_papers(
            all_papers
        )

        relevant_papers = self._filter_relevant_papers(
            unique_papers,
            query
        )

        ranked_papers = self._rank_papers(
            relevant_papers,
            query
        )

        final_papers = ranked_papers[:top_k]

        return SearchResult(
            query=query,
            papers=final_papers,
            total_found=len(relevant_papers)
        )

    def _filter_relevant_papers(
        self,
        papers,
        query: str
    ):
        query_words = {
            word.lower()
            for word in query.split()
            if len(word) > 2
        }

        relevant_papers = []

        for paper in papers:

            text = " ".join([
                paper.title or "",
                paper.abstract or ""
            ]).lower()
            matching_words=sum(
                1
                for word in query_words
                if word in text
            )

            if matching_words > 2:
                relevant_papers.append(paper)

        return relevant_papers

    def _score_paper(
        self,
        paper,
        query: str
    ) -> int:

        query_words = {
            word.lower()
            for word in query.split()
            if len(word) > 2
        }

        title = (paper.title or "").lower()
        abstract = (paper.abstract or "").lower()

        score = 0

        for word in query_words:

            if word in title:
                score += 3

            if word in abstract:
                score += 1

        return score

    def _rank_papers(
        self,
        papers,
        query: str
    ):
        return sorted(
            papers,
            key=lambda paper: self._score_paper(
                paper,
                query
            ),
            reverse=True
        )