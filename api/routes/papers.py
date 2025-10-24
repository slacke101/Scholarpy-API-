from fastapi import APIRouter, Query
from typing import List
from api.schemas import Paper
from scrapers.arxiv_scraper import search_arxiv
from scrapers.pubmed_scraper import search_pubmed
from core.utils import fetch_json  # for crossref


router = APIRouter()


async def _search_crossref(query: str, limit: int = 20):
    from api.schemas import Paper

    url = "https://api.crossref.org/works"
    params = {"query": query, "rows": limit}
    data = await fetch_json(url, params)
    items = data.get("message", {}).get("items", [])
    papers: list[Paper] = []
    for it in items:
        papers.append(
            Paper(
                title=it.get("title", [""])[0],
                authors=[
                    f"{a.get('given', '')} {a.get('family', '')}"
                    for a in it.get("author", [])
                ],
                abstract=it.get("abstract"),
                published_date="-".join(
                    str(p) for p in it.get("issued", {}).get("date-parts", [[""]])[0]
                ),
                doi=it.get("DOI"),
                url=it.get("URL"),
            )
        )
    return papers


@router.get("/", response_model=List[Paper])
async def search_papers(
    q: str = Query(..., description="Search term for papers"), limit: int = 20
):
    """Aggregate search across ArXiv, PubMed, Crossref."""
    arxiv = await search_arxiv(q, limit)
    pubmed = await search_pubmed(q, limit)
    crossref = await _search_crossref(q, limit)
    return arxiv + pubmed + crossref
