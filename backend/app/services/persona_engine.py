import json
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.logging import logger
from app.models.agent import Agent
from app.memory.breeth_engine import BreethMemoryEngine
from app.utils.constants import DEFAULT_PERSONA

class PersonaEngine:
    """
    Persona Engine for Ada (AI Security Researcher).
    Enforces voice consistency: Professional, Research-based, Technical,
    Friendly, Opinionated, Anti-clickbait, and Evidence-backed.
    """

    def __init__(self, db: Session):
        self.db = db
        self.memory_engine = BreethMemoryEngine(db)
        self._ensure_persona_in_db()

    def _ensure_persona_in_db(self) -> Agent:
        agent = self.db.query(Agent).filter(
            Agent.name == DEFAULT_PERSONA["name"],
            Agent.is_deleted == False
        ).first()
        if not agent:
            agent = Agent(
                name=DEFAULT_PERSONA["name"],
                domain=DEFAULT_PERSONA["domain"],
                characteristics=DEFAULT_PERSONA["characteristics"],
                system_prompt=DEFAULT_PERSONA["system_prompt"],
                status="ACTIVE"
            )
            self.db.add(agent)
            self.db.commit()
            self.db.refresh(agent)
        return agent

    def get_agent_profile(self) -> Dict[str, Any]:
        agent = self._ensure_persona_in_db()
        return agent.to_dict()

    def build_system_prompt(self) -> str:
        """Constructs rich persona prompt augmented with dynamic Breeth Memory context."""
        context = self.memory_engine.get_full_persona_context()
        styles = "\n- ".join(context.get("style_guidelines", []))
        prefs = "\n- ".join(context.get("editorial_preferences", []))
        
        prompt = (
            f"You are Ada, an autonomous AI Security researcher, systems engineer, and industry analyst.\n"
            f"Domain: {DEFAULT_PERSONA['domain']}\n\n"
            f"CORE CHARACTERISTICS:\n"
            f"- Professional & Research-based: Rigorous, grounded in computer science, cryptography, and empirical data.\n"
            f"- Technical yet Friendly: Clearly explain complex mechanics without dumbing down the science.\n"
            f"- Opinionated & Honest: Take a stance on security postures, guardrails, and architectural trade-offs.\n"
            f"- Anti-Clickbait: No hype, no sensationalism. Focus on real vulnerabilities, mitigation, and benchmark validity.\n"
            f"- Always cite primary sources and include explicit takeaways.\n\n"
            f"BREETH MEMORY STYLE RULES:\n- {styles}\n\n"
            f"BREETH EDITORIAL PREFERENCES:\n- {prefs}\n"
        )
        return prompt
