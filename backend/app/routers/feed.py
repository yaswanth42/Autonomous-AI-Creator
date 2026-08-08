from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.post import Post
from app.schemas.post import FeedResponse, FeedPostItem, PostResponse

router = APIRouter(tags=["Feed"])

@router.get("/api/agent/feed", response_model=FeedResponse)
def get_agent_feed(
    agentId: Optional[str] = Query(default=None, description="Optional agent UUID to filter posts"),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Hackathon Specification API: Returns autonomous posts sorted newest first.
    Each item contains id, createdAt (ISO 8601 UTC), text, rationale, sources.
    """
    posts_query = db.query(Post).filter(
        Post.status == "PUBLISHED",
        Post.is_deleted == False
    )

    if agentId:
        posts_query = posts_query.filter(Post.agent_id == agentId)

    posts = posts_query.order_by(Post.created_at.desc()).offset(offset).limit(limit).all()

    feed_items = []
    for p in posts:
        # Normalize sources to list of string URLs or structured items
        normalized_sources = []
        if isinstance(p.sources, list):
            for s in p.sources:
                if isinstance(s, dict) and "url" in s:
                    normalized_sources.append(s["url"])
                elif isinstance(s, str):
                    normalized_sources.append(s)
                else:
                    normalized_sources.append(str(s))
        elif isinstance(p.sources, str):
            normalized_sources.append(p.sources)

        # ISO 8601 UTC timestamp format (e.g. 2026-08-07T10:30:00Z)
        created_at_str = ""
        if p.created_at:
            created_at_str = p.created_at.strftime("%Y-%m-%dT%H:%M:%SZ")

        feed_items.append(
            FeedPostItem(
                id=str(p.id),
                createdAt=created_at_str,
                text=p.raw_markdown or f"**{p.title}**\n\n{p.body}",
                rationale=p.rationale or "Evaluated by 7-factor editorial decision engine and selected for high AI security significance.",
                sources=normalized_sources
            )
        )

    return FeedResponse(
        posts=feed_items
    )


@router.get("/api/feed/posts", response_model=List[PostResponse])
def get_all_posts_detailed(
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Returns rich post entities for dashboard rendering."""
    posts = db.query(Post).filter(
        Post.is_deleted == False
    ).order_by(Post.created_at.desc()).limit(limit).all()

    return [p.to_dict() for p in posts]
