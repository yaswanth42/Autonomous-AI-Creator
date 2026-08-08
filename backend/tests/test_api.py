def test_health_check(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_agent_init_endpoint(client):
    payload = {
        "name": "Ada",
        "domain": "AI Security",
        "characteristics": ["Professional", "Technical", "Opinionated"]
    }
    res = client.post("/api/agent/init", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "Ada"
    assert data["status"] == "ACTIVE"
    assert "agentId" in data

def test_agent_feed_endpoint(client):
    # Initialize agent
    client.post("/api/agent/init", json={"persona": {"name": "Ada", "domain": "AI Security"}})

    # Trigger cycle
    client.post("/api/agent/trigger")

    # Check feed
    res = client.get("/api/agent/feed")
    assert res.status_code == 200
    data = res.json()
    assert "posts" in data
    assert isinstance(data["posts"], list)
    if data["posts"]:
        first_post = data["posts"][0]
        assert "id" in first_post
        assert "createdAt" in first_post
        assert "text" in first_post
        assert "rationale" in first_post
        assert "sources" in first_post


def test_editorial_endpoints(client):
    res = client.post("/api/editorial/evaluate", json={
        "title": "Anthropic Prompt Injection Sandbox Verification",
        "content": "Formal verification of security sandboxes for LLM agent execution.",
        "source": "Anthropic Research",
        "threshold": 7.0
    })
    assert res.status_code == 200
    data = res.json()
    assert data["decision"] in ["PUBLISH", "REJECT"]
    assert "scores" in data

def test_memory_endpoints(client):
    res = client.get("/api/memory/stats")
    assert res.status_code == 200
    assert "total_memories" in res.json()

def test_analytics_dashboard_endpoint(client):
    res = client.get("/api/analytics/dashboard")
    assert res.status_code == 200
    data = res.json()
    assert "cards" in data
    assert "daily_publishing" in data
    assert "topic_categories" in data

def test_ai_usage_endpoint(client):
    res = client.get("/api/ai-usage")
    assert res.status_code == 200
    data = res.json()
    assert "summary" in data
    assert "logs" in data
