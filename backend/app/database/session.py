import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from app.core.logging import logger
from app.database.base import Base
from app.models.agent import Agent
from app.models.memory import Memory
from app.utils.constants import DEFAULT_PERSONA

# SQLite connect args
connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initializes SQLite database tables and seeds initial persona and memory presets."""
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    try:
        # Check if default agent Ada exists
        agent = db.query(Agent).filter(Agent.name == DEFAULT_PERSONA["name"], Agent.is_deleted == False).first()
        if not agent:
            logger.info("Seeding default agent Ada...")
            agent = Agent(
                name=DEFAULT_PERSONA["name"],
                domain=DEFAULT_PERSONA["domain"],
                characteristics=DEFAULT_PERSONA["characteristics"],
                system_prompt=DEFAULT_PERSONA["system_prompt"],
                status="ACTIVE"
            )
            db.add(agent)
            db.commit()
            db.refresh(agent)

        # Seed initial Breeth Memory seeds if empty
        existing_memories = db.query(Memory).filter(Memory.is_deleted == False).count()
        if existing_memories == 0:
            logger.info("Seeding initial Breeth Memory principles and writing style...")
            initial_memories = [
                Memory(
                    memory_type="STYLE",
                    category="writing_voice",
                    content="Always maintain a technical, objective, and intellectually rigorous tone. Avoid sensationalist adjectives like 'shocking' or 'revolutionary'. Cite arXiv papers, CVE numbers, or official vendor security advisories whenever possible.",
                    metadata_json=json.dumps({"persona": "Ada", "topic": "style_guide"}),
                    importance=1.0
                ),
                Memory(
                    memory_type="PREFERENCE",
                    category="editorial_policy",
                    content="Prioritize deep-dive technical insights over high-level announcements. Focus on AI security, LLM jailbreaks, agentic vulnerability mitigation, MCP protocol integrity, and verified benchmarks.",
                    metadata_json=json.dumps({"persona": "Ada", "topic": "editorial_preference"}),
                    importance=1.0
                ),
                Memory(
                    memory_type="REASONING",
                    category="decision_framework",
                    content="When evaluating a paper or model release, score novelty higher if it includes reproducible adversarial evaluations or novel red-teaming methodologies.",
                    metadata_json=json.dumps({"persona": "Ada", "topic": "scoring_heuristics"}),
                    importance=0.9
                )
            ]
            db.add_all(initial_memories)
            db.commit()
            logger.info("Breeth Memory seeded successfully.")
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")
        db.rollback()
    finally:
        db.close()
