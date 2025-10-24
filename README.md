# Scholar API

![Created by Rafael Castro & Faith Nambasa](https://img.shields.io/badge/Created%20by-Rafael%20Castro%20&%20Faith%20Nambasa-blue)


Scholar API is a FastAPI-powered micro-service that unifies access to **scholarly papers, patents, and research datasets** through a single, consistent REST interface.

- **Data sources**: PubMed, arXiv, IEEE Xplore, Zenodo, and United-States/European patent offices.
- **Persistence**: MongoDB for structured metadata, optional Azure Blob Storage for large binaries (PDFs, supplemental files).
- **Features**: Semantic search, pluggable scrapers, in-memory caching, async HTTP clients, and auto-generated OpenAPI docs.

---

## Who Is This For?

| Role                   | Why You'd Use Scholar API                                                                |
| ---------------------- | ---------------------------------------------------------------------------------------- |
| Researchers / Students | Pull literature programmatically, build dashboards, or automate systematic reviews.      |
| Data Scientists        | Feed cleaned publication & patent metadata into analytics or ML pipelines.               |
| Ed-Tech / SaaS Teams   | Embed research search capabilities in products without maintaining multiple vendor APIs. |
| Patent Analysts        | Cross-reference scientific publications with patent filings for novelty checks.          |

---

## Installation

### 1. Clone & create a virtual env

```bash
git clone https://github.com/slacke101/Scholarpy-API-.git
cd Scholarpy-API-
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment variables

Create a `.env` file or export variables:

```bash
MONGO_URI=mongodb://localhost:27017/scholar
IEEE_API_KEY=<optional>
ZENODO_TOKEN=<optional>
USE_BLOB_STORAGE=false  # set true & configure if storing PDFs in Azure
```

### 4. Run the development server

```bash
uvicorn api.main:app --reload  # http://localhost:8000/docs
```

Docker users can simply run:

```bash
docker build -t scholar-api .
docker run -p 8000:8000 -e MONGO_URI=... scholar-api
```

---

## Usage Examples

### cURL

```bash
# Search PubMed & arXiv simultaneously for "graph neural networks"
curl -X GET "http://localhost:8000/papers/search?q=graph+neural+networks&limit=25" | jq
```

### Python client

```python
import requests
resp = requests.get("http://localhost:8000/patents/search", params={"q": "battery recycling", "limit": 10})
print(resp.json())
```

---

## API Endpoints (excerpt)

| Method | Route              | Description                               |
| ------ | ------------------ | ----------------------------------------- |
| GET    | `/papers/search`   | Search across PubMed, arXiv, IEEE, Zenodo |
| GET    | `/patents/search`  | USPTO / EPO patent search                 |
| GET    | `/datasets/search` | Research datasets (Zenodo)                |
| GET    | `/health`          | Uptime, Mongo ping, cache stats           |

Interactive docs live at `/docs` (Swagger UI) and `/redoc` (ReDoc).

---

## Typical Workflows / Use Cases

1. **Literature Dashboards** – Query the API nightly to populate Kibana or Superset with fresh publication counts.
2. **Automated Alerts** – Combine with cron & email to notify researchers when new papers match a keyword.
3. **Patent-Publication Crosswalks** – Pull patents & related papers to identify white-space opportunities.
4. **Data-Driven Grant Writing** – Use aggregated publication metrics as evidence of research trends.

---

## Project Structure

```text
ScholarAPI/
├── api/          # FastAPI routers & entrypoint
├── scrapers/     # Individual source scrapers (async httpx)
├── core/         # Caching, normalization, utils
├── tests/        # Pytest suite
└── Dockerfile    # Container build
```

---

## Contributing

Pull requests are welcome! Please open an issue first to discuss your feature or bug fix.

1. Fork the repo & create your branch: `git checkout -b feat/my-feature`
2. Run lint & tests: `ruff . && pytest -q`
3. Push and open a PR.

---

## License

[MIT](LICENSE) © 2025 Scholar API Maintainers
