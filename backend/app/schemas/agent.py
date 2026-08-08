from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class AgentBase(BaseModel):
    name: str = Field(default="Ada", description="Agent persona name")
    domain: str = Field(default="AI Security", description="Domain of expertise")
    characteristics: List[str] = Field(default_factory=list, description="Personality characteristics")
    system_prompt: Optional[str] = Field(default=None, description="System prompt instructions")
    status: str = Field(default="ACTIVE", description="Agent status")

class AgentCreate(AgentBase):
    pass

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    characteristics: Optional[List[str]] = None
    system_prompt: Optional[str] = None
    status: Optional[str] = None

class AgentResponse(AgentBase):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    is_deleted: bool = False

    model_config = ConfigDict(from_attributes=True)


class PersonaNestedInput(BaseModel):
    name: Optional[str] = "Ada"
    domain: Optional[str] = "AI Security"
    characteristics: Optional[List[str]] = None
    system_prompt: Optional[str] = None

class AgentInitInput(BaseModel):
    persona: Optional[PersonaNestedInput] = None
    name: Optional[str] = None
    domain: Optional[str] = None
    characteristics: Optional[List[str]] = None
    system_prompt: Optional[str] = None

class AgentInitOutput(BaseModel):
    agentId: str
    status: Optional[str] = "ACTIVE"
    name: Optional[str] = "Ada"
    domain: Optional[str] = "AI Security"
    message: Optional[str] = "Agent initialized successfully"

