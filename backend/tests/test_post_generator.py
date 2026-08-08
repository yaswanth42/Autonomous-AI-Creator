from app.services.post_generator import PostGeneratorService
from app.services.persona_engine import PersonaEngine
from app.models.post import Post

def test_persona_engine_rules(db_session):
    pe = PersonaEngine(db_session)
    profile = pe.get_agent_profile()

    assert profile["name"] == "Ada"
    assert profile["domain"] == "AI Security"
    prompt = pe.build_system_prompt()
    assert "Ada" in prompt
    assert "Professional" in prompt

def test_post_generator_word_count_and_structure(db_session):
    pg = PostGeneratorService(db_session)
    topic = {
        "title": "OpenAI o3 Alignment & Chain-of-Thought Concealment",
        "source": "OpenAI Safety",
        "url": "https://openai.com/index/o3-safety",
        "content": "Adversarial benchmarking on reasoning models reveals new paradigms for chain of thought verification and alignment verification."
    }
    editorial_eval = {"total_score": 8.8, "decision": "PUBLISH"}

    post = pg.generate_post(topic, editorial_eval)
    assert post.id is not None
    assert post.status == "PUBLISHED"
    
    words = post.raw_markdown.split()
    assert 180 <= len(words) <= 400
    assert len(post.insights) == 3
    assert post.takeaway != ""
    assert post.hook != ""
