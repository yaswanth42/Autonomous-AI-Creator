import json
import re
import math
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from app.models.memory import Memory
from app.core.logging import logger

class BreethMemoryEngine:
    """
    Breeth Memory Cognitive Engine for Autonomous AI Personas.
    Provides semantic retrieval, episodic memory, writing style retention,
    editorial preference querying, and duplicate/novelty verification.
    """

    def __init__(self, db: Session):
        self.db = db

    def _tokenize(self, text: str) -> List[str]:
        """Simple, fast tokenizer removing punctuation and stop-words."""
        text = text.lower()
        words = re.findall(r'\b[a-z0-9_]{2,}\b', text)
        stop_words = {
            "the", "a", "an", "and", "or", "in", "on", "at", "to", "for", "of",
            "with", "is", "was", "are", "were", "this", "that", "it", "by", "from"
        }
        return [w for w in words if w not in stop_words]

    def _compute_tf_idf_vector(self, tokens: List[str], vocabulary: Dict[str, int], idfs: Dict[str, float]) -> List[float]:
        """Computes normalized TF-IDF vector."""
        tf = {}
        for token in tokens:
            tf[token] = tf.get(token, 0) + 1
        
        vector = [0.0] * len(vocabulary)
        squared_sum = 0.0
        for token, count in tf.items():
            if token in vocabulary:
                idx = vocabulary[token]
                score = (count / len(tokens)) * idfs.get(token, 1.0)
                vector[idx] = score
                squared_sum += score * score

        # Normalize vector
        magnitude = math.sqrt(squared_sum)
        if magnitude > 0:
            vector = [v / magnitude for v in vector]
        return vector

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculates cosine similarity between two unit vectors."""
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0
        return sum(a * b for a, b in zip(vec1, vec2))

    def _build_corpus_index(self, memories: List[Memory]) -> Tuple[Dict[str, int], Dict[str, float], List[List[float]]]:
        """Builds vocabulary, IDFs, and vector index for active memory items."""
        docs_tokens = [self._tokenize(m.content) for m in memories]
        num_docs = len(docs_tokens) or 1
        
        # Build vocabulary & document frequency
        doc_freq = {}
        for tokens in docs_tokens:
            seen = set(tokens)
            for token in seen:
                doc_freq[token] = doc_freq.get(token, 0) + 1

        vocabulary = {token: i for i, token in enumerate(sorted(doc_freq.keys()))}
        idfs = {token: math.log((num_docs + 1) / (df + 1)) + 1.0 for token, df in doc_freq.items()}
        
        vectors = [self._compute_tf_idf_vector(tokens, vocabulary, idfs) for tokens in docs_tokens]
        return vocabulary, idfs, vectors

    def store(
        self,
        memory_type: str,
        category: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        importance: float = 1.0
    ) -> Memory:
        """Stores a new memory node in Breeth Memory."""
        memory = Memory(
            memory_type=memory_type.upper(),
            category=category,
            content=content,
            metadata_json=json.dumps(metadata or {}),
            importance=importance
        )
        self.db.add(memory)
        self.db.commit()
        self.db.refresh(memory)
        logger.info(f"Stored Breeth Memory [{memory.memory_type}] ID={memory.id[:8]} category={category}")
        return memory

    def store_post(self, post_id: str, title: str, text: str, rationale: str, sources: List[Any]) -> Memory:
        """Stores a published post into Breeth memory."""
        content = f"Title: {title}\nRationale: {rationale}\nPost: {text}"
        metadata = {
            "post_id": post_id,
            "title": title,
            "sources_count": len(sources),
            "published_at": datetime.now(timezone.utc).isoformat()
        }
        return self.store(
            memory_type="POST",
            category="published_post",
            content=content,
            metadata=metadata,
            importance=1.0
        )

    def store_rejected_topic(self, topic_title: str, reason: str, scores: Dict[str, Any], url: Optional[str] = None) -> Memory:
        """Stores a rejected topic and rationale into Breeth memory to prevent repeating evaluations."""
        content = f"Rejected Topic: {topic_title}\nReason: {reason}\nScores: {json.dumps(scores)}"
        metadata = {
            "topic_title": topic_title,
            "url": url,
            "scores": scores,
            "reason": reason
        }
        return self.store(
            memory_type="REJECTED",
            category="rejected_topic",
            content=content,
            metadata=metadata,
            importance=0.8
        )

    def store_editorial_preference(self, preference_text: str, domain: str = "AI Security") -> Memory:
        """Stores an editorial rule or preference."""
        return self.store(
            memory_type="PREFERENCE",
            category="editorial_policy",
            content=preference_text,
            metadata={"domain": domain},
            importance=1.0
        )

    def store_writing_style(self, style_guideline: str) -> Memory:
        """Stores a writing style rule for Ada."""
        return self.store(
            memory_type="STYLE",
            category="persona_style",
            content=style_guideline,
            metadata={"persona": "Ada"},
            importance=1.0
        )

    def store_reasoning(self, context: str, decision: str, rationale: str) -> Memory:
        """Stores an agent reasoning chain for historical consistency."""
        content = f"Context: {context}\nDecision: {decision}\nRationale: {rationale}"
        return self.store(
            memory_type="REASONING",
            category="decision_framework",
            content=content,
            metadata={"decision": decision},
            importance=0.9
        )

    def store_publishing_history(self, summary_text: str, cadence_hours: int = 4) -> Memory:
        """Stores publishing cadence and volume metrics."""
        return self.store(
            memory_type="PUBLISHING_HISTORY",
            category="cadence_log",
            content=summary_text,
            metadata={"cadence_hours": cadence_hours},
            importance=0.7
        )

    def query_relevant(
        self,
        query: str,
        memory_types: Optional[List[str]] = None,
        top_k: int = 5,
        min_similarity: float = 0.1
    ) -> List[Dict[str, Any]]:
        """
        Retrieves top-k relevant memories ranked by semantic relevance and importance.
        Updates access count and last_accessed_at for retrieved nodes.
        """
        q = self.db.query(Memory).filter(Memory.is_deleted == False)
        if memory_types:
            types_upper = [t.upper() for t in memory_types]
            q = q.filter(Memory.memory_type.in_(types_upper))
        
        memories = q.all()
        if not memories:
            return []

        vocabulary, idfs, vectors = self._build_corpus_index(memories)
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        query_vec = self._compute_tf_idf_vector(query_tokens, vocabulary, idfs)

        scored_results = []
        for memory, vec in zip(memories, vectors):
            sim = self._cosine_similarity(query_vec, vec)
            # Weighted by importance score
            final_score = sim * (0.8 + 0.2 * memory.importance)
            if sim >= min_similarity or len(memories) <= 3:
                scored_results.append((final_score, sim, memory))

        # Sort descending by score
        scored_results.sort(key=lambda x: x[0], reverse=True)
        top_matches = scored_results[:top_k]

        results = []
        for final_score, sim, memory in top_matches:
            memory.record_access()
            results.append({
                "id": memory.id,
                "memory_type": memory.memory_type,
                "category": memory.category,
                "content": memory.content,
                "similarity": round(sim, 4),
                "score": round(final_score, 4),
                "importance": memory.importance,
                "metadata": memory.metadata_dict,
                "created_at": memory.created_at.isoformat() if memory.created_at else None
            })

        self.db.commit()
        return results

    def check_duplicate_and_novelty(
        self,
        topic_title: str,
        topic_content: str = "",
        url: Optional[str] = None
    ) -> Tuple[bool, float, Optional[Dict[str, Any]]]:
        """
        Queries Breeth Memory against published posts and rejected topics.
        Returns: (is_duplicate: bool, highest_similarity: float, closest_memory: Optional[dict])
        """
        query_text = f"{topic_title} {topic_content[:200]}"
        matches = self.query_relevant(
            query=query_text,
            memory_types=["POST", "REJECTED"],
            top_k=3,
            min_similarity=0.25
        )

        if not matches:
            return False, 0.0, None

        highest = matches[0]
        sim = highest["similarity"]
        # If similarity >= 0.72 or exact URL match in metadata, consider duplicate
        is_dup = sim >= 0.72
        if url and highest.get("metadata", {}).get("url") == url:
            is_dup = True
            sim = 1.0

        return is_dup, sim, highest

    def get_full_persona_context(self) -> Dict[str, Any]:
        """
        Gathers complete editorial policies, style guides, and reasoning patterns
        to feed directly into every agent decision.
        """
        memories = self.db.query(Memory).filter(
            Memory.is_deleted == False,
            Memory.memory_type.in_(["STYLE", "PREFERENCE", "REASONING"])
        ).all()

        style_rules = [m.content for m in memories if m.memory_type == "STYLE"]
        preferences = [m.content for m in memories if m.memory_type == "PREFERENCE"]
        reasonings = [m.content for m in memories if m.memory_type == "REASONING"]

        recent_posts = self.db.query(Memory).filter(
            Memory.is_deleted == False,
            Memory.memory_type == "POST"
        ).order_by(Memory.created_at.desc()).limit(5).all()

        return {
            "style_guidelines": style_rules,
            "editorial_preferences": preferences,
            "reasoning_frameworks": reasonings,
            "recent_published_topics": [p.metadata_dict.get("title", "") for p in recent_posts if p.metadata_dict.get("title")]
        }
