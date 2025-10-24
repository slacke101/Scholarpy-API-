import httpx
from typing import List
from api.schemas import Paper
import feedparser
from urllib.parse import urlencode
from core.normalize import normalize_author_list

ARXIV_ENDPOINT = "https://export.arxiv.org/api/query"


def _build_query(query: str, limit: int):
    params = {
        "search_query": query,
        "start": 0,
        "max_results": limit,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    return f"{ARXIV_ENDPOINT}?{urlencode(params)}"


async def search_arxiv(query: str, limit: int = 20):
    """Fetch results from ArXiv API and map to Paper model list."""
    url = _build_query(query, limit)

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, headers={"User-Agent": "ScholarAPI/0.1"})
        resp.raise_for_status()
        feed = feedparser.parse(resp.text)

    from api.schemas import Paper  # local import to avoid circular

    papers: list[Paper] = []
    for entry in feed.entries:
        papers.append(
            Paper(
                title=entry.title,
                authors=normalize_author_list([a.name for a in entry.authors]),
                abstract=entry.get("summary"),
                published_date=entry.get("published"),
                doi=entry.get("arxiv_doi"),
                url=entry.get("id"),
            )
        )
    return papers
