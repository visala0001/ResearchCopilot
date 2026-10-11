
import time
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone

import requests

from app.config.settings import SEMANTIC_SCHOLAR_API_KEY
from app.models.paper import Paper


class SemanticScholarTool:
    BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

    def __init__(
        self,
        timeout: int = 15,
        max_retries: int = 2,
        min_request_interval: float = 1.0,
    ):
        self.timeout = timeout
        self.max_retries = max_retries
        self.min_request_interval = min_request_interval
        self._last_request_time = 0.0

    def _wait_for_rate_limit(self):
        elapsed = time.monotonic() - self._last_request_time
        remaining = self.min_request_interval - elapsed

        if remaining > 0:
            time.sleep(remaining)

    def _retry_delay(self, response, attempt: int) -> float:
        retry_after = response.headers.get("Retry-After")

        if retry_after:
            try:
                return max(0.0, float(retry_after))
            except ValueError:
                try:
                    retry_date = parsedate_to_datetime(retry_after)

                    if retry_date.tzinfo is None:
                        retry_date = retry_date.replace(
                            tzinfo=timezone.utc
                        )

                    return max(
                        0.0,
                        (retry_date - datetime.now(timezone.utc)).total_seconds(),
                    )
                except (TypeError, ValueError, OverflowError):
                    pass

        # If the server gives no usable Retry-After value,
        # wait longer before retrying a rate-limited request.
        return 5.0 * (2 ** attempt)

    def search_papers(
        self,
        query: str,
        limit: int = 10,
    ) -> list[Paper]:
        if not query or not query.strip():
            raise ValueError("Search query cannot be empty.")

        if limit <= 0:
            raise ValueError("Limit must be greater than 0.")

        params = {
            "query": query.strip(),
            "limit": limit,
            "fields": (
                "paperId,title,abstract,authors,"
                "year,venue,url,citationCount"
            ),
        }

        headers = {}

        if SEMANTIC_SCHOLAR_API_KEY:
            headers["x-api-key"] = SEMANTIC_SCHOLAR_API_KEY

        for attempt in range(self.max_retries + 1):
            self._wait_for_rate_limit()
            self._last_request_time = time.monotonic()

            try:
                response = requests.get(
                    self.BASE_URL,
                    params=params,
                    headers=headers,
                    timeout=self.timeout,
                )

            except requests.exceptions.Timeout as exc:
                if attempt == self.max_retries:
                    raise RuntimeError(
                        "Semantic Scholar request timed out."
                    ) from exc

                time.sleep(2 ** attempt)
                continue

            except requests.exceptions.RequestException as exc:
                raise RuntimeError(
                    f"Semantic Scholar request failed: {exc}"
                ) from exc

            if response.status_code == 429:
                if attempt == self.max_retries:
                    retry_after = response.headers.get("Retry-After")
                    message = "Semantic Scholar rate limit reached."

                    if retry_after:
                        message += (
                            f" Server requested retry after "
                            f"{retry_after}."
                        )

                    raise RuntimeError(message)

                time.sleep(self._retry_delay(response, attempt))
                continue

            response.raise_for_status()
            break

        data = response.json()
        papers = []

        for item in data.get("data", []):
            authors = [
                author.get("name")
                for author in item.get("authors", [])
                if author.get("name")
            ]

            papers.append(
                Paper(
                    paper_id=item.get("paperId"),
                    title=item.get("title"),
                    abstract=item.get("abstract"),
                    authors=authors,
                    year=item.get("year"),
                    venue=item.get("venue"),
                    url=item.get("url"),
                    citation_count=item.get("citationCount"),
                )
            )

        return papers
