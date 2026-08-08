from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.post import Post
from app.models.search_history import SearchHistory
from app.utils.constants import TOPIC_KEYWORDS

router = APIRouter(prefix="/api/sources", tags=["Sources"])

@router.get("")
def get_sources_overview(db: Session = Depends(get_db)):
    """Returns source breakdown, authoritative domains, and discovery keywords."""
    posts = db.query(Post).filter(Post.is_deleted == False).all()
    searches = db.query(SearchHistory).filter(SearchHistory.is_deleted == False).count()

    source_counts: Dict[str, int] = {}
    for p in posts:
        for s in p.sources:
            src_name = s.get("source", "Web Search")
            source_counts[src_name] = source_counts.get(src_name, 0) + 1

    trusted_authorities = [
        {"name": "Anthropic Research", "domain": "research.anthropic.com", "trust_tier": "TIER_1", "status": "ACTIVE"},
        {"name": "OpenAI Safety", "domain": "openai.com/research", "trust_tier": "TIER_1", "status": "ACTIVE"},
        {"name": "Google DeepMind", "domain": "deepmind.google", "trust_tier": "TIER_1", "status": "ACTIVE"},
        {"name": "Meta AI Research", "domain": "ai.meta.com/research", "trust_tier": "TIER_1", "status": "ACTIVE"},
        {"name": "HuggingFace Security", "domain": "huggingface.co/blog", "trust_tier": "TIER_1", "status": "ACTIVE"},
        {"name": "Microsoft Research", "domain": "microsoft.com/research", "trust_tier": "TIER_1", "status": "ACTIVE"},
        {"name": "arXiv CS.CR / AI", "domain": "arxiv.org", "trust_tier": "TIER_1", "status": "ACTIVE"},
        {"name": "OWASP GenAI Security", "domain": "owasp.org", "trust_tier": "TIER_1", "status": "ACTIVE"}
    ]

    return {
        "keywords": TOPIC_KEYWORDS,
        "total_searches": searches,
        "source_distribution": [{"source": k, "count": v} for k, v in source_counts.items()],
        "trusted_authorities": trusted_authorities
    }
