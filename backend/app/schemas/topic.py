from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class TopicItem(BaseModel):
    title: str
    url: Optional[str] = None
    content: str
    source: str = "Tavily"
    published_date: Optional[str] = None
    score: Optional[float] = None
    raw_json: Optional[Dict[str, Any]] = None

class TopicSearchRequest(BaseModel):
    query: Optional[str] = None
    keywords: Optional[List[str]] = None
    max_results: int = 10
    include_raw: bool = False

class TopicSearchResponse(BaseModel):
    query: str
    provider: str
    results_count: int
    topics: List[TopicItem]
    timestamp: str
