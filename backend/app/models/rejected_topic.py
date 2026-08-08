import json
from typing import Dict, Any, Optional
from sqlalchemy import Column, String, Text, Float, Index
from app.database.base import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin

class RejectedTopic(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "rejected_topics"

    title = Column(String(255), nullable=False, index=True)
    url = Column(String(500), nullable=True, index=True)
    source = Column(String(100), nullable=False, default="Tavily", index=True)
    reason = Column(Text, nullable=False)
    score_breakdown_json = Column(Text, nullable=False, default="{}")
    total_score = Column(Float, nullable=False, default=0.0, index=True)
    
    # 7-factor scores
    novelty = Column(Float, nullable=False, default=0.0)
    importance = Column(Float, nullable=False, default=0.0)
    trustworthiness = Column(Float, nullable=False, default=0.0)
    trending_score = Column(Float, nullable=False, default=0.0)
    technical_value = Column(Float, nullable=False, default=0.0)
    community_impact = Column(Float, nullable=False, default=0.0)
    duplicate_penalty = Column(Float, nullable=False, default=0.0)

    __table_args__ = (
        Index("ix_rejected_topics_score_created", "total_score", "created_at"),
    )

    @property
    def score_breakdown(self) -> Dict[str, Any]:
        try:
            return json.loads(self.score_breakdown_json)
        except Exception:
            return {}

    @score_breakdown.setter
    def score_breakdown(self, val: Dict[str, Any]):
        self.score_breakdown_json = json.dumps(val)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "source": self.source,
            "reason": self.reason,
            "score_breakdown": self.score_breakdown,
            "total_score": self.total_score,
            "novelty": self.novelty,
            "importance": self.importance,
            "trustworthiness": self.trustworthiness,
            "trending_score": self.trending_score,
            "technical_value": self.technical_value,
            "community_impact": self.community_impact,
            "duplicate_penalty": self.duplicate_penalty,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_deleted": self.is_deleted
        }
