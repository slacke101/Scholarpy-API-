from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class Paper(BaseModel):
    title: str
    authors: List[str]
    abstract: Optional[str] = None
    published_date: Optional[str] = None  # ISO format
    doi: Optional[str] = None
    url: Optional[HttpUrl] = None


class Patent(BaseModel):
    title: str
    patent_number: str
    inventors: List[str]
    abstract: Optional[str] = None
    published_date: Optional[str] = None
    url: Optional[HttpUrl] = None


class Dataset(BaseModel):
    title: str
    creators: List[str]
    description: Optional[str] = None
    published_date: Optional[str] = None
    url: Optional[HttpUrl] = None
