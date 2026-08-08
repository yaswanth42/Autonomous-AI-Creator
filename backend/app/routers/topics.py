from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.search_history import SearchHistory
from app.schemas.topic import TopicSearchRequest, TopicSearchResponse, TopicItem
from app.services.topic_discovery import TopicDiscoveryService

router = APIRouter(prefix="/api/topics", tags=["Topics"])

@router.get("/latest")
def get_latest_topics(db: Session = Depends(get_db)):
    """Returns recent search history and topics discovered."""
    history = db.query(SearchHistory).filter(
        SearchHistory.is_deleted == False
    ).order_by(SearchHistory.created_at.desc()).limit(10).all()

    return [h.to_dict() for h in history]

@router.post("/search", response_model=TopicSearchResponse)
def search_live_topics(request: Optional[TopicSearchRequest] = None, db: Session = Depends(get_db)):
    """Triggers live search across target keywords."""
    svc = TopicDiscoveryService(db)
    keywords = request.keywords if request and request.keywords else None
    max_results = request.max_results if request else 10

    topics = svc.discover_latest_topics(keywords=keywords, max_total=max_results, filter_duplicates=True)
    
    topic_items = [
        TopicItem(
            title=t["title"],
            url=t.get("url"),
            content=t.get("content", ""),
            source=t.get("source", "Tavily"),
            published_date=t.get("published_date"),
            score=t.get("score")
        )
        for t in topics
    ]

    return TopicSearchResponse(
        query=", ".join(keywords) if keywords else "Default AI Security Keywords",
        provider="Tavily" if svc.api_key else "Tavily (Simulated Live)",
        results_count=len(topic_items),
        topics=topic_items,
        timestamp=datetime.now(timezone.utc).isoformat()
    )
