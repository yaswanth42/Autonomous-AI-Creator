import json
from typing import Dict, Any, Optional
from sqlalchemy import Column, String, Text, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.database.base import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin

class EditorialHistory(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "editorial_history"

    topic_title = Column(String(255), nullable=False, index=True)
    topic_url = Column(String(500), nullable=True, index=True)
    decision = Column(String(50), nullable=False, default="REJECT", index=True) # PUBLISH or REJECT
    total_score = Column(Float, nullable=False, default=0.0, index=True)
    scores_json = Column(Text, nullable=False, default="{}")
    reasoning = Column(Text, nullable=False)
    
    agent_id = Column(String(36), ForeignKey("agents.id", ondelete="SET NULL"), nullable=True, index=True)
    post_id = Column(String(36), ForeignKey("posts.id", ondelete="SET NULL"), nullable=True, index=True)

    # Relationships
    agent = relationship("Agent", back_populates="editorial_history")
    post = relationship("Post", back_populates="editorial_history")

    __table_args__ = (
        Index("ix_editorial_decision_created", "decision", "created_at"),
    )

    @property
    def scores(self) -> Dict[str, Any]:
        try:
            return json.loads(self.scores_json)
        except Exception:
            return {}

    @scores.setter
    def scores(self, val: Dict[str, Any]):
        self.scores_json = json.dumps(val)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "topic_title": self.topic_title,
            "topic_url": self.topic_url,
            "decision": self.decision,
            "total_score": self.total_score,
            "scores": self.scores,
            "reasoning": self.reasoning,
            "agent_id": self.agent_id,
            "post_id": self.post_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_deleted": self.is_deleted
        }
