import httpx


async def fetch_json(url: str, params: dict | None = None):
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
