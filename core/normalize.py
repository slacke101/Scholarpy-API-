"""Functions for normalizing raw scraper data into schema models."""

from typing import Dict, Any


def normalize_author_list(raw_authors: Any) -> list[str]:
    if isinstance(raw_authors, str):
        return [raw_authors]
    if isinstance(raw_authors, list):
        return [str(a) for a in raw_authors]
    return []
