import json
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy import Column, String, Text, Float, Integer, DateTime, Index
from app.database.base import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin

class Memory(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "memories"

    # Types: POST, REJECTED, PREFERENCE, STYLE, REASONING, PUBLISHING_HISTORY, SYSTEM
    memory_type = Column(String(50), nullable=False, default="POST", index=True)
    category = Column(String(100), nullable=False, default="general", index=True)
    content = Column(Text, nullable=False)
    embedding_json = Column(Text, nullable=True) # Vector embedding serialization
    metadata_json = Column(Text, nullable=False, default="{}")
    importance = Column(Float, nullable=False, default=1.0, index=True)
    access_count = Column(Integer, nullable=False, default=0)
    last_accessed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    __table_args__ = (
        Index("ix_memories_type_category", "memory_type", "category"),
        Index("ix_memories_type_created", "memory_type", "created_at"),
    )

    @property
    def metadata_dict(self) -> Dict[str, Any]:
        try:
            return json.loads(self.metadata_json)
        except Exception:
            return {}

    @metadata_dict.setter
    def metadata_dict(self, val: Dict[str, Any]):
        self.metadata_json = json.dumps(val)

    @property
    def embedding(self) -> Optional[List[float]]:
        if not self.embedding_json:
            return None
        try:
            return json.loads(self.embedding_json)
        except Exception:
            return None

    @embedding.setter
    def embedding(self, val: Optional[List[float]]):
        if val is not None:
            self.embedding_json = json.dumps(val)
        else:
            self.embedding_json = None

    def record_access(self):
        self.access_count += 1
        self.last_accessed_at = datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "memory_type": self.memory_type,
            "category": self.category,
            "content": self.content,
            "metadata": self.metadata_dict,
            "importance": self.importance,
            "access_count": self.access_count,
            "last_accessed_at": self.last_accessed_at.isoformat() if self.last_accessed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_deleted": self.is_deleted
        }
