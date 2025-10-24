from fastapi import APIRouter, Query
from typing import List
from api.schemas import Patent
from scrapers.usp_patent_scraper import search_usp_patents
from scrapers.local_patent_scraper import search_local_patents


router = APIRouter()


@router.get("/", response_model=List[Patent])
async def search_patents(
    q: str = Query(..., description="Search term for patents"), limit: int = 20
):
    """Search patents via USPTO PatentsView."""
    results = await search_usp_patents(q, limit)
    if not results:
        results = search_local_patents(q, limit)
    return results
