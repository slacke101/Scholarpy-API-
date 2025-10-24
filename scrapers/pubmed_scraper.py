import httpx
from typing import List
from core.normalize import normalize_author_list

# TODO(Faith): Implement exponential backoff with `tenacity` (or custom retry) when PubMed returns
#              HTTP 429/503 to respect rate-limits.
# TODO(Faith): Cache successful ESearch/ESummary responses in `core.cache` to reduce external calls.
# TODO(Faith): Swap placeholder abstract field; use efetch or dedicated endpoint to retrieve full abstract text.
# TODO(Faith): When full-text PDF is available, upload it to Azure Blob and store URL in the Paper model.

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


async def _esearch(query: str, limit: int):
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": limit,
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{BASE_URL}/esearch.fcgi", params=params)
        r.raise_for_status()
        data = r.json()
        return data["esearchresult"].get("idlist", [])


async def _esummary(ids: list[str]):
    if not ids:
        return []
    params = {
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "json",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{BASE_URL}/esummary.fcgi", params=params)
        r.raise_for_status()
        return r.json()["result"]


async def search_pubmed(query: str, limit: int = 20):
    from api.schemas import Paper

    ids = await _esearch(query, limit)
    summaries = await _esummary(ids)

    papers: List[Paper] = []
    for pid in ids:
        item = summaries.get(pid)
        if not item:
            continue
        papers.append(
            Paper(
                title=item.get("title"),
                authors=normalize_author_list(
                    [au.get("name") for au in item.get("authors", [])]
                ),
                abstract=item.get("elocationid"),
                published_date=item.get("pubdate"),
                doi=item.get("elocationid"),
                url=f"https://pubmed.ncbi.nlm.nih.gov/{pid}/",
            )
        )
    return papers
