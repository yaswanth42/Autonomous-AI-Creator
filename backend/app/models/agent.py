import json
from typing import List, Dict, Any, Optional
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from app.database.base import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin

class Agent(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "agents"

    name = Column(String(100), nullable=False, default="Ada", index=True)
    domain = Column(String(100), nullable=False, default="AI Security", index=True)
    characteristics_json = Column(Text, nullable=False, default="[]")
    system_prompt = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="ACTIVE", index=True)

    # Relationships
    posts = relationship("Post", back_populates="agent", cascade="all, delete-orphan")
    editorial_history = relationship("EditorialHistory", back_populates="agent", cascade="all, delete-orphan")

    @property
    def characteristics(self) -> List[str]:
        try:
            return json.loads(self.characteristics_json)
        except Exception:
            return []

    @characteristics.setter
    def characteristics(self, val: List[str]):
        self.characteristics_json = json.dumps(val)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "domain": self.domain,
            "characteristics": self.characteristics,
            "system_prompt": self.system_prompt,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_deleted": self.is_deleted
        }
