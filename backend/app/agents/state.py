from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict, total=False):
    topic: Dict[str, Any]
    memory_context: Dict[str, Any]
    editorial_eval: Dict[str, Any]
    persona_name: str
    persona_domain: str
    persona_characteristics: List[str]
    system_prompt: str
    draft_title: str
    draft_hook: str
    draft_body: str
    draft_insights: List[str]
    draft_takeaway: str
    raw_markdown: str
    rationale: str
    sources: List[Dict[str, Any]]
    status: str
    error: Optional[str]
