import os, gzip, json
from functools import lru_cache
from typing import Iterator, Dict, Any, List

BULK_PATH = os.getenv("PATENTS_BULK_PATH", "patents.jsonl.gz")


def _iter_patents() -> Iterator[Dict[str, Any]]:
    """Yield patent records from local PatentsView bulk JSONL(.gz) file."""
    if not os.path.exists(BULK_PATH):
        return
    opener = gzip.open if BULK_PATH.endswith(".gz") else open
    with opener(BULK_PATH, "rt", encoding="utf-8") as f:
        for line in f:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


@lru_cache(maxsize=1)
def load_index() -> List[Dict[str, Any]]:
    """Load all patent docs into memory once (simplistic)."""
    return list(_iter_patents())
