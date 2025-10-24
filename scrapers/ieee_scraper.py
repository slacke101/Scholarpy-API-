import httpx
from typing import List
from api.schemas import Paper


async def search_ieee(query: str, limit: int = 20) -> List[Paper]:
    """Search IEEE Xplore and return normalized Paper objects (placeholder)."""
    return []
