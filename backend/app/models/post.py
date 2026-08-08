import json
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from sqlalchemy import Column, String, Text, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.database.base import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin

class Post(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "posts"

    agent_id = Column(String(36), ForeignKey("agents.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    hook = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    insights_json = Column(Text, nullable=False, default="[]")
    takeaway = Column(Text, nullable=False)
    raw_markdown = Column(Text, nullable=False)
    rationale = Column(Text, nullable=False)
    sources_json = Column(Text, nullable=False, default="[]")
    score = Column(Float, nullable=False, default=8.0, index=True)
    status = Column(String(50), nullable=False, default="PUBLISHED", index=True)
    published_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # Relationships
    agent = relationship("Agent", back_populates="posts")
    editorial_history = relationship("EditorialHistory", back_populates="post", uselist=False)

    __table_args__ = (
        Index("ix_posts_published_created", "published_at", "created_at"),
    )

    @property
    def insights(self) -> List[str]:
        try:
            return json.loads(self.insights_json)
        except Exception:
            return []

    @insights.setter
    def insights(self, val: List[str]):
        self.insights_json = json.dumps(val)

    @property
    def sources(self) -> List[Dict[str, Any]]:
        try:
            return json.loads(self.sources_json)
        except Exception:
            return []

    @sources.setter
    def sources(self, val: List[Any]):
        self.sources_json = json.dumps(val)

    @property
    def text(self) -> str:
        """Convenience property matching the full generated markdown text for hackathon API"""
        return self.raw_markdown

    def to_feed_dict(self) -> Dict[str, Any]:
        """Matches exact Hackathon API spec: id, createdAt, text, rationale, sources"""
        return {
            "id": self.id,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "text": self.raw_markdown,
            "rationale": self.rationale,
            "sources": self.sources
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "title": self.title,
            "hook": self.hook,
            "body": self.body,
            "insights": self.insights,
            "takeaway": self.takeaway,
            "raw_markdown": self.raw_markdown,
            "rationale": self.rationale,
            "sources": self.sources,
            "score": self.score,
            "status": self.status,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_deleted": self.is_deleted
        }
