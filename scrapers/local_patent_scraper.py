from typing import List
from rapidfuzz import process, fuzz
from api.schemas import Patent
from core.patent_store import load_index


def search_local_patents(query: str, limit: int = 20) -> List[Patent]:
    docs = load_index()
    if not docs:
        return []
    # Use rapid text matching on title
    matches = process.extract(
        query,
        {i: d.get("patent_title", "") for i, d in enumerate(docs)},
        scorer=fuzz.token_set_ratio,
        limit=limit,
    )
    patents: List[Patent] = []
    for idx, score, _ in matches:
        d = docs[idx]
        patents.append(
            Patent(
                title=d.get("patent_title"),
                patent_number=d.get("patent_number"),
                inventors=[inv.get("inventor_name") for inv in d.get("inventors", [])],
                abstract=d.get("patent_abstract"),
                published_date=d.get("patent_date"),
            )
        )
    return patents
