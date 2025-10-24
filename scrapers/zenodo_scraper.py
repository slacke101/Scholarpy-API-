import httpx
from typing import List

BASE_URL = "https://zenodo.org/api/records"


async def search_zenodo(query: str, limit: int = 20):
    from api.schemas import Dataset

    params = {"q": query, "size": limit}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(BASE_URL, params=params)
        r.raise_for_status()
        hits = r.json().get("hits", {}).get("hits", [])

    datasets: List[Dataset] = []
    for hit in hits:
        meta = hit["metadata"]
        datasets.append(
            Dataset(
                title=meta.get("title"),
                creators=[c.get("name") for c in meta.get("creators", [])],
                description=meta.get("description"),
                published_date=meta.get("publication_date"),
                url=hit.get("links", {}).get("html"),
            )
        )
    return datasets
