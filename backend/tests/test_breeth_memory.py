from app.memory.breeth_engine import BreethMemoryEngine
from app.services.memory_service import MemoryService
from app.models.memory import Memory

def test_breeth_memory_store_and_search(db_session):
    engine = BreethMemoryEngine(db_session)
    mem1 = engine.store(
        memory_type="POST",
        category="published_post",
        content="Anthropic Model Context Protocol MCP security sandboxing and vulnerability mitigations.",
        importance=1.5
    )

    mem2 = engine.store(
        memory_type="PREFERENCE",
        category="editorial_rule",
        content="Avoid clickbait sensationalism and always maintain technical academic tone.",
        importance=1.2
    )

    assert mem1.id is not None
    assert mem2.id is not None

    # Search for MCP
    matches = engine.query_relevant("MCP server sandbox isolation", top_k=5, min_similarity=0.01)
    assert len(matches) > 0
    top_match = matches[0]
    assert "MCP" in top_match["content"]
    assert top_match["similarity"] > 0.01

def test_duplicate_detection(db_session):
    engine = BreethMemoryEngine(db_session)
    engine.store_post(
        post_id="test-post-1",
        title="Google DeepMind SynthID Cryptographic Watermarking",
        text="Cryptographic watermarking protocol for AI agent generated code.",
        rationale="High technical impact",
        sources=[{"title": "DeepMind", "url": "https://deepmind.google/synthid"}]
    )

    # Check identical topic
    is_dup, sim, match = engine.check_duplicate_and_novelty(
        topic_title="Google DeepMind SynthID Cryptographic Watermarking",
        topic_content="Cryptographic watermarking protocol for AI agent generated code.",
        url="https://deepmind.google/synthid"
    )

    assert is_dup is True
    assert sim >= 0.7

def test_memory_service_stats(db_session):
    svc = MemoryService(db_session)
    svc.engine.store("STYLE", "writing_style", "Tone must be authoritative yet accessible.")
    stats = svc.get_stats()

    assert stats["total_memories"] >= 1
    assert "STYLE" in stats["by_type"]
