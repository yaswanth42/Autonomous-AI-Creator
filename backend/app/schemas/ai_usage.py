from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class AIUsageLogItem(BaseModel):
    id: str
    timestamp: str
    milestone: str
    prompt_title: str
    prompt_text: str
    output_summary: str
    model: str
    tokens_used: int
    latency_ms: float
    status: str

class AIUsageResponse(BaseModel):
    summary: Dict[str, Any]
    logs: List[AIUsageLogItem]
