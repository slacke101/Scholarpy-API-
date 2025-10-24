import httpx
from typing import List

BASE_URL = "https://search.patentsview.org/api/v1/patents/query"


def _build_body(query: str, limit: int):
    return {
        "q": {"_text_any": {"patent_title": query}},
        "f": [
            "patent_number",
            "patent_title",
            "patent_date",
            "inventor_first_name",
            "inventor_last_name",
            "patent_abstract",
        ],
        "o": {"per_page": limit},
    }


async def search_usp_patents(query: str, limit: int = 20):
    from api.schemas import Patent

    body = _build_body(query, limit)
    headers = {
        "User-Agent": "ScholarAPI/0.1 (mailto:your_email@example.com)",
        "Referer": "https://patentsview.org/",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(
        timeout=10, follow_redirects=True, headers=headers
    ) as client:
        r = await client.post(BASE_URL, json=body)
        if r.status_code == 403:
            # Return empty list to avoid crashing API; PatentsView blocked us
            return []
        r.raise_for_status()
        data = r.json()
        patents_json = data.get("patents", []) if isinstance(data, dict) else []

    patents: List[Patent] = []
    for p in patents_json:
        inventors = [
            f"{inv.get('inventor_first_name', '')} {inv.get('inventor_last_name', '')}"
            for inv in p.get("inventors", [])
        ]
        patents.append(
            Patent(
                title=p.get("patent_title"),
                patent_number=p.get("patent_number"),
                inventors=inventors,
                abstract=p.get("patent_abstract"),
                published_date=p.get("patent_date"),
                url=f"https://patents.google.com/patent/US{p.get('patent_number')}"
                if p.get("patent_number")
                else None,
            )
        )
    return patents
