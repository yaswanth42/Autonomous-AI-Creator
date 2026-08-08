from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.agent import Agent
from app.models.memory import Memory
from app.models.post import Post
from app.schemas.agent import AgentInitInput, AgentInitOutput, AgentResponse
from app.services.persona_engine import PersonaEngine
from app.services.scheduler_service import scheduler_service
from app.core.ai_tracker import ai_tracker
from app.core.logging import logger
from app.utils.constants import DEFAULT_PERSONA

router = APIRouter(prefix="/api/agent", tags=["Agent"])

@router.post("/init", response_model=AgentInitOutput)
def init_agent(input_data: Optional[AgentInitInput] = None, db: Session = Depends(get_db)):
    """
    Hackathon Specification API: Initializes the autonomous AI persona.
    Returns agentId, status, name, domain, message.
    """
    # Extract name and domain from either nested 'persona' or root fields
    req_name = None
    req_domain = None
    req_chars = None
    req_prompt = None

    if input_data:
        if input_data.persona:
            req_name = input_data.persona.name
            req_domain = input_data.persona.domain
            req_chars = input_data.persona.characteristics
            req_prompt = input_data.persona.system_prompt
        if not req_name and input_data.name:
            req_name = input_data.name
        if not req_domain and input_data.domain:
            req_domain = input_data.domain
        if not req_chars and input_data.characteristics:
            req_chars = input_data.characteristics
        if not req_prompt and input_data.system_prompt:
            req_prompt = input_data.system_prompt

    name = req_name or DEFAULT_PERSONA["name"]
    domain = req_domain or DEFAULT_PERSONA["domain"]
    characteristics = req_chars or DEFAULT_PERSONA["characteristics"]
    system_prompt = req_prompt or DEFAULT_PERSONA["system_prompt"]

    agent = db.query(Agent).filter(Agent.name == name, Agent.is_deleted == False).first()

    if not agent:
        agent = Agent(
            name=name,
            domain=domain,
            characteristics=characteristics,
            system_prompt=system_prompt,
            status="ACTIVE"
        )
        db.add(agent)
        db.commit()
        db.refresh(agent)
    else:
        # Update existing agent properties if provided
        if input_data and input_data.domain:
            agent.domain = domain
        if input_data and input_data.characteristics:
            agent.characteristics = characteristics
        if input_data and input_data.system_prompt:
            agent.system_prompt = system_prompt
        db.commit()
        db.refresh(agent)

    ai_tracker.log_event(
        milestone="Prompt 9: API",
        prompt_title="Agent Initialization API",
        prompt_text=f"POST /api/agent/init payload: {input_data.model_dump() if input_data else {}}",
        output_summary=f"Agent '{agent.name}' initialized with ID={agent.id}",
        model="gpt-4o-mini"
    )

    return AgentInitOutput(
        agentId=agent.id,
        status=agent.status,
        name=agent.name,
        domain=agent.domain,
        message=f"Autonomous persona '{agent.name}' ({agent.domain}) initialized successfully."
    )

@router.get("/status")
def get_agent_status(db: Session = Depends(get_db)):
    """Returns real-time status of agent, scheduler, and memory statistics."""
    agent = db.query(Agent).filter(Agent.name == DEFAULT_PERSONA["name"], Agent.is_deleted == False).first()
    if not agent:
        pe = PersonaEngine(db)
        agent = pe._ensure_persona_in_db()

    posts_count = db.query(Post).filter(Post.agent_id == agent.id, Post.is_deleted == False).count()
    memory_count = db.query(Memory).filter(Memory.is_deleted == False).count()
    sched_status = scheduler_service.get_status()

    return {
        "agent": agent.to_dict(),
        "posts_published": posts_count,
        "memories_stored": memory_count,
        "scheduler": sched_status
    }

@router.post("/trigger")
def trigger_autonomous_cycle():
    """Manually triggers one complete autonomous cycle immediately."""
    result = scheduler_service.trigger_now()
    return {
        "message": "Autonomous cycle executed successfully.",
        "result": result
    }
