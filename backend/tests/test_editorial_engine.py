from app.services.editorial_engine import EditorialDecisionEngine
from app.models.rejected_topic import RejectedTopic
from app.models.editorial_history import EditorialHistory

def test_editorial_engine_publish_decision(db_session):
    engine = EditorialDecisionEngine(db_session, threshold=7.0)
    result = engine.evaluate_topic(
        title="Model Context Protocol (MCP) Security Analysis: Sandbox Escape & Tool Poisoning Risks",
        content="A rigorous technical evaluation of MCP server implementations reveals architectural vulnerabilities in automated agent tool calling and prompt injection relaying.",
        url="https://research.anthropic.com/mcp-security",
        source="Anthropic Research"
    )

    assert result["decision"] == "PUBLISH"
    assert result["total_score"] >= 7.0
    assert result["scores"]["novelty"] > 0
    assert result["scores"]["trustworthiness"] >= 9.0

    history = db_session.query(EditorialHistory).first()
    assert history is not None
    assert history.decision == "PUBLISH"

def test_editorial_engine_reject_decision(db_session):
    engine = EditorialDecisionEngine(db_session, threshold=7.5)
    result = engine.evaluate_topic(
        title="Top 5 AI Crypto Trading Bots Guaranteed to Make You Rich",
        content="Check out these quick passive income AI tools for crypto trading!",
        url="https://scam-crypto.xyz/bots",
        source="Crypto Spam Blog"
    )

    assert result["decision"] == "REJECT"
    assert result["total_score"] < 7.5
    assert "Rejected by Editorial Engine" in result["reasoning"]

    rejected = db_session.query(RejectedTopic).first()
    assert rejected is not None
    assert "Crypto" in rejected.title
