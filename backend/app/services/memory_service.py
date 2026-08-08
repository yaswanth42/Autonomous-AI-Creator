from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.memory.breeth_engine import BreethMemoryEngine
from app.models.memory import Memory

class MemoryService:
    """Service layer exposing Breeth Memory operations across the application."""

    def __init__(self, db: Session):
        self.db = db
        self.engine = BreethMemoryEngine(db)

    def query_memories(
        self,
        query: str,
        memory_types: Optional[List[str]] = None,
        limit: int = 5,
        min_similarity: float = 0.1
    ) -> List[Dict[str, Any]]:
        return self.engine.query_relevant(
            query=query,
            memory_types=memory_types,
            top_k=limit,
            min_similarity=min_similarity
        )

    def store_post(self, post_id: str, title: str, text: str, rationale: str, sources: List[Any]) -> Memory:
        return self.engine.store_post(post_id, title, text, rationale, sources)

    def store_rejected(self, title: str, reason: str, scores: Dict[str, Any], url: Optional[str] = None) -> Memory:
        return self.engine.store_rejected_topic(title, reason, scores, url)

    def store_preference(self, text: str, domain: str = "AI Security") -> Memory:
        return self.engine.store_editorial_preference(text, domain)

    def store_style(self, style_rule: str) -> Memory:
        return self.engine.store_writing_style(style_rule)

    def store_reasoning(self, context: str, decision: str, rationale: str) -> Memory:
        return self.engine.store_reasoning(context, decision, rationale)

    def get_agent_context(self) -> Dict[str, Any]:
        return self.engine.get_full_persona_context()

    def check_duplicate(self, title: str, content: str = "", url: Optional[str] = None):
        return self.engine.check_duplicate_and_novelty(title, content, url)

    def get_stats(self) -> Dict[str, Any]:
        all_memories = self.db.query(Memory).filter(Memory.is_deleted == False).all()
        by_type: Dict[str, int] = {}
        for m in all_memories:
            by_type[m.memory_type] = by_type.get(m.memory_type, 0) + 1

        top_accessed = sorted(all_memories, key=lambda m: m.access_count, reverse=True)[:5]
        return {
            "total_memories": len(all_memories),
            "by_type": by_type,
            "top_accessed": [m.to_dict() for m in top_accessed]
        }
