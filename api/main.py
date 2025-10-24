from fastapi import FastAPI
from api.routes import papers, patents, datasets

app = FastAPI(title="Scholar API", version="0.1.0")

# TODO(Faith): Add Pagination dependency (limit, offset, sort) and apply to all routers.
# TODO(Faith): Implement Health and Metrics endpoint at `/health` exposing uptime, MongoDB ping, cache stats.
# TODO(Faith): Integrate Prometheus exporter (`prometheus-fastapi-instrumentator`).
# TODO(Faith): Switch to `motor` (async Mongo client) and ensure all DB operations are awaited.

# Include routers
app.include_router(papers.router, prefix="/papers", tags=["Papers"])
app.include_router(patents.router, prefix="/patents", tags=["Patents"])
app.include_router(datasets.router, prefix="/datasets", tags=["Datasets"])


@app.get("/")
async def root():
    return {"message": "Welcome to Scholar API"}
