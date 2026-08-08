from datetime import datetime, timezone
from app.models.agent import Agent
from app.models.post import Post
from app.models.rejected_topic import RejectedTopic
from app.models.memory import Memory
from app.models.search_history import SearchHistory
from app.models.editorial_history import EditorialHistory
from app.models.ai_usage_log import AIUsageLog

def test_agent_model_creation(db_session):
    agent = Agent(
        name="Ada",
        domain="AI Security",
        characteristics=["Professional", "Technical"],
        system_prompt="Test Prompt",
        status="ACTIVE"
    )
    db_session.add(agent)
    db_session.commit()

    assert agent.id is not None
    assert agent.name == "Ada"
    assert agent.is_deleted is False

    d = agent.to_dict()
    assert d["name"] == "Ada"
    assert d["domain"] == "AI Security"

def test_post_model_and_feed_dict(db_session):
    agent = Agent(name="Ada", domain="AI Security", system_prompt="Autonomous AI security specialist.")
    db_session.add(agent)
    db_session.commit()

    post = Post(
        agent_id=agent.id,
        title="Testing Post",
        hook="Hook text",
        body="Body text",
        insights=["Insight 1", "Insight 2"],
        takeaway="Strategic takeaway",
        raw_markdown="**Testing Post**\n\nHook\n\nBody",
        rationale="High score",
        sources=[{"title": "Test Source", "url": "https://test.org"}],
        score=8.5,
        status="PUBLISHED"
    )
    db_session.add(post)
    db_session.commit()

    feed_d = post.to_feed_dict()
    assert feed_d["id"] == post.id
    assert "createdAt" in feed_d
    assert feed_d["text"] == post.raw_markdown
    assert feed_d["rationale"] == "High score"
    assert len(feed_d["sources"]) == 1

def test_soft_delete(db_session):
    mem = Memory(
        memory_type="POST",
        category="published_post",
        content="Test cognitive content"
    )
    db_session.add(mem)
    db_session.commit()

    mem.soft_delete()
    db_session.commit()

    assert mem.is_deleted is True
    assert mem.deleted_at is not None
