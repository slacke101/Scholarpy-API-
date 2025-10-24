from fastapi import APIRouter, Query
from typing import List
from api.schemas import Dataset
from scrapers.zenodo_scraper import search_zenodo


router = APIRouter()


@router.get("/", response_model=List[Dataset])
async def search_datasets(
    q: str = Query(..., description="Search term for datasets"), limit: int = 20
):
    """Search datasets via Zenodo."""
    return await search_zenodo(q, limit)
