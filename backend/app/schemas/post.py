from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict

class PostBase(BaseModel):
    title: str
    hook: str
    body: str
    insights: List[str] = Field(default_factory=list)
    takeaway: str
    raw_markdown: str
    rationale: str
    sources: List[Dict[str, Any]] = Field(default_factory=list)
    score: float = 8.0
    status: str = "PUBLISHED"

class PostCreate(PostBase):
    agent_id: str

class PostResponse(PostBase):
    id: str
    agent_id: str
    published_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    is_deleted: bool = False

    model_config = ConfigDict(from_attributes=True)

# Exact Hackathon Feed Spec schema
class FeedPostItem(BaseModel):
    id: str
    createdAt: str
    text: str
    rationale: str
    sources: List[Any] = Field(default_factory=list)

class FeedResponse(BaseModel):
    posts: List[FeedPostItem]

