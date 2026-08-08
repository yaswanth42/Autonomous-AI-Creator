from datetime import datetime, timezone
from typing import Dict, Any
from sqlalchemy import Column, String, Text, Integer, Float, Index
from app.database.base import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin

class AIUsageLog(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "ai_usage_logs"

    milestone = Column(String(100), nullable=False, index=True)
    prompt_title = Column(String(255), nullable=False, index=True)
    prompt_text = Column(Text, nullable=False)
    output_summary = Column(Text, nullable=False)
    model = Column(String(100), nullable=False, default="gpt-4o-mini")
    tokens_used = Column(Integer, nullable=False, default=0)
    latency_ms = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), nullable=False, default="SUCCESS", index=True)

    __table_args__ = (
        Index("ix_ai_usage_milestone_created", "milestone", "created_at"),
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "milestone": self.milestone,
            "prompt_title": self.prompt_title,
            "prompt_text": self.prompt_text,
            "output_summary": self.output_summary,
            "model": self.model,
            "tokens_used": self.tokens_used,
            "latency_ms": self.latency_ms,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_deleted": self.is_deleted
        }
