from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict

class EditorialScoreBreakdown(BaseModel):
    novelty: float = Field(..., ge=0.0, le=10.0)
    importance: float = Field(..., ge=0.0, le=10.0)
    trustworthiness: float = Field(..., ge=0.0, le=10.0)
    trending_score: float = Field(..., ge=0.0, le=10.0)
    technical_value: float = Field(..., ge=0.0, le=10.0)
    community_impact: float = Field(..., ge=0.0, le=10.0)
    duplicate_penalty: float = Field(default=0.0, ge=0.0, le=10.0)

class EditorialEvaluationRequest(BaseModel):
    title: str
    url: Optional[str] = None
    content: str
    source: Optional[str] = "Tavily"
    threshold: Optional[float] = 7.0

class EditorialEvaluationResponse(BaseModel):
    decision: str # PUBLISH or REJECT
    total_score: float
    threshold: float
    scores: EditorialScoreBreakdown
    reasoning: str
    topic_title: str
    topic_url: Optional[str] = None
    agent_name: str = "Ada"

class RejectedTopicResponse(BaseModel):
    id: str
    title: str
    url: Optional[str] = None
    source: str
    reason: str
    total_score: float
    score_breakdown: Dict[str, Any]
    novelty: float
    importance: float
    trustworthiness: float
    trending_score: float
    technical_value: float
    community_impact: float
    created_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

