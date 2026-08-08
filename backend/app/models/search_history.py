import json
from typing import List, Dict, Any, Optional
from sqlalchemy import Column, String, Text, Integer, Index
from app.database.base import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin

class SearchHistory(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "search_history"

    query = Column(String(255), nullable=False, index=True)
    provider = Column(String(100), nullable=False, default="Tavily", index=True)
    raw_results_count = Column(Integer, nullable=False, default=0)
    filtered_count = Column(Integer, nullable=False, default=0)
    results_json = Column(Text, nullable=False, default="[]")

    __table_args__ = (
        Index("ix_search_history_created", "created_at"),
    )

    @property
    def results(self) -> List[Dict[str, Any]]:
        try:
            return json.loads(self.results_json)
        except Exception:
            return []

    @results.setter
    def results(self, val: List[Any]):
        self.results_json = json.dumps(val)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "query": self.query,
            "provider": self.provider,
            "raw_results_count": self.raw_results_count,
            "filtered_count": self.filtered_count,
            "results": self.results,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_deleted": self.is_deleted
        }
